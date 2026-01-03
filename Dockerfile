# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install additional packages needed for production
RUN pip install --no-cache-dir \
    streamlit==1.40.2 \
    ollama==0.4.10 \
    sentence-transformers==5.2.0 \
    chromadb==1.4.0 \
    torch==2.9.1 \
    PyPDF2==4.0.2 \
    python-docx==1.1.2 \
    loguru==0.7.3 \
    pandas==2.2.3

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p data/vector_store logs

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run the application
CMD ["streamlit", "run", "src/ui/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
