"""
Chat API endpoints
"""
from fastapi import APIRouter, HTTPException, Depends, status
from src.api.models.schemas import ChatRequest, ChatResponse, ErrorResponse
from src.core.rag_engine import RAGEngine
from src.core.vector_store import VectorStore
from src.auth.database import UsageDB
from src.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api", tags=["chat"])

# Usage limits per tier
TIER_LIMITS = {
    "free": 10,      # 10 queries per day
    "pro": 1000,     # 1000 queries per day
    "enterprise": -1  # Unlimited
}

# Global RAG engine instance
_rag_engine = None


def get_rag_engine() -> RAGEngine:
    """Get or create RAG engine instance"""
    global _rag_engine
    if _rag_engine is None:
        try:
            vector_store = VectorStore()
            _rag_engine = RAGEngine(
                vector_store=vector_store,
                llm_model="tinyllama",
                top_k=2
            )
            logger.info("RAG engine initialized for API")
        except Exception as e:
            logger.error(f"Failed to initialize RAG engine: {e}")
            raise HTTPException(status_code=500, detail="Failed to initialize RAG engine")
    return _rag_engine


@router.post("/chat", response_model=ChatResponse, responses={500: {"model": ErrorResponse}})
async def chat(
    request: ChatRequest,
    rag_engine: RAGEngine = Depends(get_rag_engine),
    current_user: dict = None  # Optional - if not provided, uses anonymous access
):
    """
    Chat endpoint - ask questions and get AI-powered answers

    - **question**: Your question (1-1000 characters)
    - **session_id**: Optional session ID for conversation tracking

    **Authentication**: Optional. Authenticated users get higher rate limits.

    **Rate Limits**:
    - Anonymous: 10 queries/day
    - Free tier: 10 queries/day
    - Pro tier: 1000 queries/day
    - Enterprise: Unlimited

    Returns answer with source documents used for context.
    """
    try:
        # Check usage limits if user is authenticated
        if current_user:
            user_id = current_user["id"]
            tier = current_user.get("tier", "free")
            limit = TIER_LIMITS.get(tier, 10)

            # Check if limit exceeded (unless unlimited)
            if limit > 0:
                usage_count = UsageDB.get_user_usage_count(user_id, action="chat", days=1)
                if usage_count >= limit:
                    raise HTTPException(
                        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                        detail=f"Daily limit exceeded. Upgrade to Pro for more queries! ({usage_count}/{limit})"
                    )

        logger.info(f"Processing chat request: {request.question[:50]}...")

        # Query the RAG engine
        result = rag_engine.query(request.question, return_context=True)

        # Format sources
        sources = []
        if "context" in result and result["context"].get("documents"):
            for i, doc in enumerate(result["context"]["documents"]):
                source = {
                    "content": doc[:200] + "..." if len(doc) > 200 else doc,
                    "metadata": result["context"]["metadatas"][i] if i < len(result["context"]["metadatas"]) else {}
                }
                sources.append(source)

        response = ChatResponse(
            answer=result["answer"],
            sources=sources,
            num_sources=result.get("num_sources", 0),
            session_id=request.session_id
        )

        # Track usage if authenticated
        if current_user:
            UsageDB.log_action(current_user["id"], "chat", f"question: {request.question[:100]}")

        logger.info(f"Chat response generated with {response.num_sources} sources")
        return response

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing chat request: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating response: {str(e)}"
        )
