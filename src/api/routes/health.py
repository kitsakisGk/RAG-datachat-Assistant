"""
Health check and metrics endpoints
"""
from fastapi import APIRouter, Depends
import time
from src.api.models.schemas import HealthResponse, MetricsResponse
from src.core.rag_engine import RAGEngine
from src.llm.ollama_client import get_ollama_client
from src.utils.logger import get_logger
from src.api.routes.chat import get_rag_engine

logger = get_logger(__name__)
router = APIRouter(prefix="/api", tags=["monitoring"])

# Track service start time
_start_time = time.time()
_request_count = 0
_total_response_time = 0.0


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint

    Returns service status and availability of dependencies.
    """
    try:
        # Check Ollama availability
        ollama_client = get_ollama_client(model="tinyllama")
        ollama_available = ollama_client.is_available()

        return HealthResponse(
            status="healthy" if ollama_available else "degraded",
            version="1.0.0",
            ollama_available=ollama_available
        )

    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return HealthResponse(
            status="unhealthy",
            version="1.0.0",
            ollama_available=False
        )


@router.get("/metrics", response_model=MetricsResponse)
async def get_metrics(rag_engine: RAGEngine = Depends(get_rag_engine)):
    """
    Get service metrics

    Returns performance metrics and statistics.
    """
    try:
        total_docs = rag_engine.vector_store.count()
        uptime = time.time() - _start_time

        avg_response_time = 0.0
        if _request_count > 0:
            avg_response_time = _total_response_time / _request_count

        return MetricsResponse(
            total_documents=total_docs,
            total_queries=_request_count,
            avg_response_time=round(avg_response_time, 2),
            uptime=round(uptime, 2)
        )

    except Exception as e:
        logger.error(f"Error getting metrics: {e}")
        return MetricsResponse(
            total_documents=0,
            total_queries=_request_count,
            avg_response_time=0.0,
            uptime=round(time.time() - _start_time, 2)
        )


def track_request(response_time: float):
    """Track request for metrics"""
    global _request_count, _total_response_time
    _request_count += 1
    _total_response_time += response_time
