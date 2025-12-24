"""
Embedding generation using Sentence Transformers
"""
from typing import List, Union
import numpy as np
from sentence_transformers import SentenceTransformer
from src.utils.logger import get_logger

logger = get_logger(__name__)


class EmbeddingGenerator:
    """Generate embeddings for text using sentence transformers"""

    def __init__(self, model_name: str = "BAAI/bge-base-en-v1.5"):
        """
        Initialize the embedding generator

        Args:
            model_name: Name of the sentence transformer model
        """
        self.model_name = model_name
        self.model = None
        logger.info(f"Initializing embedding generator with model: {model_name}")

    def load_model(self):
        """Load the embedding model"""
        if self.model is None:
            logger.info(f"Loading model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            logger.info(f"Model loaded successfully. Embedding dimension: {self.get_dimension()}")

    def get_dimension(self) -> int:
        """
        Get the embedding dimension

        Returns:
            Dimension of embeddings
        """
        if self.model is None:
            self.load_model()
        return self.model.get_sentence_embedding_dimension()

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text

        Args:
            text: Input text

        Returns:
            Embedding vector as list of floats
        """
        if self.model is None:
            self.load_model()

        # Generate embedding
        embedding = self.model.encode(text, convert_to_numpy=True)

        return embedding.tolist()

    def generate_embeddings(self, texts: List[str], batch_size: int = 32) -> List[List[float]]:
        """
        Generate embeddings for multiple texts

        Args:
            texts: List of input texts
            batch_size: Batch size for processing

        Returns:
            List of embedding vectors
        """
        if self.model is None:
            self.load_model()

        logger.info(f"Generating embeddings for {len(texts)} texts")

        # Generate embeddings in batches
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            convert_to_numpy=True,
            show_progress_bar=True
        )

        logger.info(f"Generated {len(embeddings)} embeddings")

        return embeddings.tolist()

    def compute_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """
        Compute cosine similarity between two embeddings

        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector

        Returns:
            Cosine similarity score (0 to 1)
        """
        # Convert to numpy arrays
        vec1 = np.array(embedding1)
        vec2 = np.array(embedding2)

        # Compute cosine similarity
        similarity = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

        return float(similarity)


# Global embedding generator instance
_embedding_generator = None


def get_embedding_generator(model_name: str = "BAAI/bge-base-en-v1.5") -> EmbeddingGenerator:
    """
    Get or create global embedding generator instance

    Args:
        model_name: Name of the sentence transformer model

    Returns:
        EmbeddingGenerator instance
    """
    global _embedding_generator

    if _embedding_generator is None:
        _embedding_generator = EmbeddingGenerator(model_name)

    return _embedding_generator


__all__ = ["EmbeddingGenerator", "get_embedding_generator"]
