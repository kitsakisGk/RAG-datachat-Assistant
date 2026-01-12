# Production Dockerfile for RAG DataChat Assistant
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install core dependencies (minimal for API)
RUN pip install --no-cache-dir \
    fastapi==0.109.0 \
    uvicorn[standard]==0.27.0 \
    pydantic==2.5.3 \
    python-multipart==0.0.6 \
    python-dotenv==1.0.0 \
    pyjwt==2.8.0 \
    email-validator==2.1.0 \
    sentence-transformers==2.2.2 \
    chromadb==0.4.22 \
    ollama==0.1.6 \
    PyPDF2==3.0.1 \
    python-docx==1.1.0 \
    loguru==0.7.2 \
    pandas==2.1.4 \
    psycopg2-binary==2.9.9 \
    sqlalchemy==2.0.25

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p data/vector_store data logs

# Expose API port
EXPOSE 8000

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8000/api/health || exit 1

# Run the FastAPI application
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
