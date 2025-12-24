"""
Vector store implementation using ChromaDB
"""
from typing import List, Dict, Optional, Any
import chromadb
from chromadb.config import Settings
from pathlib import Path
from src.utils.logger import get_logger
from src.embeddings.embeddings import get_embedding_generator

logger = get_logger(__name__)


class VectorStore:
    """ChromaDB-based vector store for RAG"""

    def __init__(
        self,
        collection_name: str = "datachat_collection",
        persist_directory: Optional[str] = None
    ):
        """
        Initialize vector store

        Args:
            collection_name: Name of the collection
            persist_directory: Directory to persist the database
        """
        self.collection_name = collection_name

        # Set default persist directory
        if persist_directory is None:
            persist_directory = str(
                Path(__file__).parent.parent.parent / "data" / "vector_store" / "chroma_db"
            )

        self.persist_directory = persist_directory

        # Create directory if it doesn't exist
        Path(self.persist_directory).mkdir(parents=True, exist_ok=True)

        logger.info(f"Initializing ChromaDB at: {self.persist_directory}")

        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=self.persist_directory,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )

        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"description": "RAG DataChat Assistant vector store"}
        )

        # Initialize embedding generator
        self.embedding_generator = get_embedding_generator()

        logger.info(f"Vector store initialized. Collection: {self.collection_name}")

    def add_documents(
        self,
        documents: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None
    ) -> List[str]:
        """
        Add documents to the vector store

        Args:
            documents: List of document texts
            metadatas: Optional metadata for each document
            ids: Optional IDs for documents (auto-generated if not provided)

        Returns:
            List of document IDs
        """
        if not documents:
            logger.warning("No documents to add")
            return []

        # Generate IDs if not provided
        if ids is None:
            existing_count = self.collection.count()
            ids = [f"doc_{existing_count + i}" for i in range(len(documents))]

        # Create default metadata if not provided
        if metadatas is None:
            metadatas = [{"source": "unknown"} for _ in documents]

        logger.info(f"Adding {len(documents)} documents to vector store")

        # Generate embeddings
        embeddings = self.embedding_generator.generate_embeddings(documents)

        # Add to collection
        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )

        logger.info(f"Successfully added {len(documents)} documents")

        return ids

    def search(
        self,
        query: str,
        n_results: int = 5,
        where: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Search for similar documents

        Args:
            query: Search query
            n_results: Number of results to return
            where: Optional metadata filter

        Returns:
            Dictionary containing ids, documents, distances, and metadatas
        """
        logger.info(f"Searching for: '{query}' (top {n_results} results)")

        # Generate query embedding
        query_embedding = self.embedding_generator.generate_embedding(query)

        # Search collection
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where
        )

        logger.info(f"Found {len(results['ids'][0])} results")

        # Format results
        formatted_results = {
            "ids": results["ids"][0] if results["ids"] else [],
            "documents": results["documents"][0] if results["documents"] else [],
            "distances": results["distances"][0] if results["distances"] else [],
            "metadatas": results["metadatas"][0] if results["metadatas"] else []
        }

        return formatted_results

    def get_by_ids(self, ids: List[str]) -> Dict[str, Any]:
        """
        Get documents by IDs

        Args:
            ids: List of document IDs

        Returns:
            Dictionary containing documents and metadatas
        """
        results = self.collection.get(ids=ids)
        return results

    def delete_by_ids(self, ids: List[str]):
        """
        Delete documents by IDs

        Args:
            ids: List of document IDs to delete
        """
        logger.info(f"Deleting {len(ids)} documents")
        self.collection.delete(ids=ids)

    def count(self) -> int:
        """
        Get total number of documents in collection

        Returns:
            Number of documents
        """
        return self.collection.count()

    def reset(self):
        """Reset the collection (delete all documents)"""
        logger.warning("Resetting vector store - all documents will be deleted")
        self.client.delete_collection(name=self.collection_name)
        self.collection = self.client.create_collection(
            name=self.collection_name,
            metadata={"description": "RAG DataChat Assistant vector store"}
        )
        logger.info("Vector store reset complete")

    def get_collection_info(self) -> Dict[str, Any]:
        """
        Get information about the collection

        Returns:
            Dictionary with collection statistics
        """
        count = self.count()
        return {
            "name": self.collection_name,
            "count": count,
            "persist_directory": self.persist_directory
        }


__all__ = ["VectorStore"]
