"""
Application configuration
Loads from environment variables with sensible defaults
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file if it exists
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path)

# Environment
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
IS_PRODUCTION = ENVIRONMENT == "production"

# Database
DATABASE_TYPE = os.getenv("DATABASE_TYPE", "sqlite")
SQLITE_PATH = os.getenv("SQLITE_PATH", "data/users.db")
DATABASE_URL = os.getenv("DATABASE_URL", "")

# Ollama
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "tinyllama")

# Vector Store
VECTOR_STORE_PATH = os.getenv("VECTOR_STORE_PATH", "data/vector_store/chroma_db")

# API
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))

# JWT
JWT_SECRET = os.getenv("JWT_SECRET", "development-secret-change-in-production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24

# CORS
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


def get_database_url() -> str:
    """Get the appropriate database URL based on configuration"""
    if DATABASE_TYPE == "postgresql" and DATABASE_URL:
        return DATABASE_URL
    elif DATABASE_TYPE == "sqlite":
        return f"sqlite:///{SQLITE_PATH}"
    else:
        # Fallback to SQLite
        return f"sqlite:///{SQLITE_PATH}"


# Print config on import (only in development)
if not IS_PRODUCTION:
    print(f"🔧 Environment: {ENVIRONMENT}")
    print(f"💾 Database: {DATABASE_TYPE}")
    print(f"🤖 Ollama: {OLLAMA_BASE_URL} ({OLLAMA_MODEL})")
    print(f"🔑 JWT Secret: {'***' if IS_PRODUCTION else JWT_SECRET[:20] + '...'}")
