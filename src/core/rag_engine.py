"""
Main RAG (Retrieval-Augmented Generation) engine
"""
from typing import List, Dict, Optional, Any
from src.core.vector_store import VectorStore
from src.llm.ollama_client import get_ollama_client
from src.llm.prompt_templates import (
    RAG_QA_TEMPLATE,
    SYSTEM_PROMPTS,
    CONVERSATION_TEMPLATE
)
from src.utils.logger import get_logger

logger = get_logger(__name__)


class RAGEngine:
    """Main RAG engine for question answering"""

    def __init__(
        self,
        vector_store: Optional[VectorStore] = None,
        llm_model: str = "mistral",
        top_k: int = 5,
        similarity_threshold: float = 0.7
    ):
        """
        Initialize RAG engine

        Args:
            vector_store: VectorStore instance
            llm_model: LLM model name
            top_k: Number of documents to retrieve
            similarity_threshold: Minimum similarity score
        """
        self.vector_store = vector_store or VectorStore()
        self.llm_client = get_ollama_client(model=llm_model)
        self.top_k = top_k
        self.similarity_threshold = similarity_threshold
        self.conversation_history = []

        logger.info(f"RAG Engine initialized with model: {llm_model}, top_k: {top_k}")

    def add_documents(
        self,
        documents: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None
    ) -> List[str]:
        """
        Add documents to the knowledge base

        Args:
            documents: List of document texts
            metadatas: Optional metadata for documents

        Returns:
            List of document IDs
        """
        logger.info(f"Adding {len(documents)} documents to knowledge base")
        return self.vector_store.add_documents(documents, metadatas)

    def retrieve_context(
        self,
        query: str,
        n_results: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Retrieve relevant context for a query

        Args:
            query: User query
            n_results: Number of results (uses top_k if not specified)

        Returns:
            Dictionary with retrieved documents and metadata
        """
        n_results = n_results or self.top_k

        logger.info(f"Retrieving context for query: '{query}'")

        # Search vector store
        results = self.vector_store.search(query, n_results=n_results)

        # Filter by similarity threshold
        filtered_results = {
            "ids": [],
            "documents": [],
            "distances": [],
            "metadatas": []
        }

        for i, distance in enumerate(results["distances"]):
            # ChromaDB uses L2 distance - lower is better
            # Accept all results with distance < 2.0 (very permissive for testing)
            # TODO: Tune this threshold based on your data
            if distance <= 2.0:
                filtered_results["ids"].append(results["ids"][i])
                filtered_results["documents"].append(results["documents"][i])
                filtered_results["distances"].append(distance)
                filtered_results["metadatas"].append(results["metadatas"][i])

        logger.info(f"Retrieved {len(filtered_results['documents'])} relevant documents")

        return filtered_results

    def format_context(self, retrieved_docs: Dict[str, Any]) -> str:
        """
        Format retrieved documents into context string

        Args:
            retrieved_docs: Dictionary from retrieve_context

        Returns:
            Formatted context string
        """
        if not retrieved_docs["documents"]:
            return "No relevant context found."

        context_parts = []
        for i, doc in enumerate(retrieved_docs["documents"]):
            metadata = retrieved_docs["metadatas"][i]
            source = metadata.get("source", "unknown")
            context_parts.append(f"[Document {i+1} - Source: {source}]\n{doc}\n")

        return "\n".join(context_parts)

    def generate_answer(
        self,
        question: str,
        context: str,
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Generate answer using LLM

        Args:
            question: User question
            context: Retrieved context
            system_prompt: Optional system prompt

        Returns:
            Generated answer
        """
        # Use default system prompt if not provided
        if system_prompt is None:
            system_prompt = SYSTEM_PROMPTS["document_qa"]

        # Format the prompt
        prompt = RAG_QA_TEMPLATE.format(
            context=context,
            question=question
        )

        logger.info("Generating answer with LLM")

        # Generate response
        try:
            answer = self.llm_client.generate(
                prompt=prompt,
                system_prompt=system_prompt,
                temperature=0.7
            )
            return answer.strip()
        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            return f"Error generating answer: {str(e)}"

    def query(
        self,
        question: str,
        return_context: bool = False
    ) -> Dict[str, Any]:
        """
        Main query method - retrieve context and generate answer

        Args:
            question: User question
            return_context: Whether to return retrieved context

        Returns:
            Dictionary with answer and optional context
        """
        logger.info(f"Processing query: '{question}'")

        # Retrieve relevant context
        retrieved_docs = self.retrieve_context(question)

        # Format context
        context = self.format_context(retrieved_docs)

        # Generate answer
        answer = self.generate_answer(question, context)

        # Build response
        response = {
            "question": question,
            "answer": answer,
            "num_sources": len(retrieved_docs["documents"])
        }

        if return_context:
            response["context"] = retrieved_docs

        logger.info("Query processed successfully")

        return response

    def chat(
        self,
        question: str,
        use_history: bool = True,
        return_context: bool = False
    ) -> Dict[str, Any]:
        """
        Chat with conversation history

        Args:
            question: User question
            use_history: Whether to use conversation history
            return_context: Whether to return retrieved context

        Returns:
            Dictionary with answer and optional context
        """
        # Get context from vector store
        retrieved_docs = self.retrieve_context(question)
        context = self.format_context(retrieved_docs)

        # Build prompt with history
        if use_history and self.conversation_history:
            history_text = "\n".join([
                f"User: {msg['user']}\nAssistant: {msg['assistant']}"
                for msg in self.conversation_history[-3:]  # Last 3 exchanges
            ])
            prompt = CONVERSATION_TEMPLATE.format(
                history=history_text,
                context=context,
                question=question
            )
        else:
            prompt = RAG_QA_TEMPLATE.format(
                context=context,
                question=question
            )

        # Generate answer
        answer = self.llm_client.generate(
            prompt=prompt,
            system_prompt=SYSTEM_PROMPTS["general_qa"],
            temperature=0.7
        )

        # Update conversation history
        self.conversation_history.append({
            "user": question,
            "assistant": answer
        })

        # Build response
        response = {
            "question": question,
            "answer": answer.strip(),
            "num_sources": len(retrieved_docs["documents"])
        }

        if return_context:
            response["context"] = retrieved_docs

        return response

    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        logger.info("Conversation history cleared")

    def get_stats(self) -> Dict[str, Any]:
        """
        Get RAG engine statistics

        Returns:
            Dictionary with stats
        """
        return {
            "total_documents": self.vector_store.count(),
            "conversation_length": len(self.conversation_history),
            "top_k": self.top_k,
            "similarity_threshold": self.similarity_threshold
        }


__all__ = ["RAGEngine"]
