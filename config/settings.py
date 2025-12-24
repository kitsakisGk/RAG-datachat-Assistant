"""
Configuration settings for RAG DataChat Assistant
"""
import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""

    # Project paths
    PROJECT_ROOT: Path = Path(__file__).parent.parent
    DATA_DIR: Path = PROJECT_ROOT / "data"
    RAW_DATA_DIR: Path = DATA_DIR / "raw"
    PROCESSED_DATA_DIR: Path = DATA_DIR / "processed"
    VECTOR_STORE_DIR: Path = DATA_DIR / "vector_store"

    # Application
    APP_NAME: str = "RAG DataChat Assistant"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True

    # API Settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_RELOAD: bool = True

    # LLM Settings
    LLM_PROVIDER: str = "ollama"  # Options: ollama, openai
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "mistral"
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4"

    # Embedding Settings
    EMBEDDING_MODEL: str = "BAAI/bge-base-en-v1.5"
    EMBEDDING_DIMENSION: int = 768

    # Vector Database
    VECTOR_DB: str = "chromadb"  # Options: chromadb, qdrant
    CHROMADB_PATH: Path = VECTOR_STORE_DIR / "chroma_db"
    QDRANT_URL: Optional[str] = None
    QDRANT_API_KEY: Optional[str] = None
    COLLECTION_NAME: str = "datachat_collection"

    # Query Settings
    MAX_QUERY_RESULTS: int = 10000
    QUERY_TIMEOUT: int = 30  # seconds
    CACHE_ENABLED: bool = True
    CACHE_TTL: int = 3600  # seconds (1 hour)

    # Database Connection
    DEFAULT_DB_TYPE: str = "sqlite"
    MAX_CONNECTIONS: int = 5
    CONNECTION_TIMEOUT: int = 10

    # Security
    ALLOW_WRITE_QUERIES: bool = False
    ENABLE_QUERY_LOGGING: bool = True
    SANITIZE_INPUTS: bool = True

    # RAG Settings
    RETRIEVAL_TOP_K: int = 5
    SIMILARITY_THRESHOLD: float = 0.7
    CONTEXT_WINDOW_SIZE: int = 4096

    # UI Settings
    STREAMLIT_PORT: int = 8501
    THEME: str = "light"

    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()


# Create necessary directories
def create_directories():
    """Create required directories if they don't exist"""
    directories = [
        settings.RAW_DATA_DIR,
        settings.PROCESSED_DATA_DIR,
        settings.VECTOR_STORE_DIR,
        settings.CHROMADB_PATH,
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    create_directories()
    print("Settings loaded successfully")
    print(f"Project Root: {settings.PROJECT_ROOT}")
    print(f"LLM Provider: {settings.LLM_PROVIDER}")
    print(f"Vector DB: {settings.VECTOR_DB}")
