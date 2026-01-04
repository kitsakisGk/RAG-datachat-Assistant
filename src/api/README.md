# RAG DataChat Assistant API

Production-ready REST API for the RAG DataChat Assistant.

## Quick Start

### Run the API

```bash
# Activate virtual environment
.\venv\Scripts\activate

# Start the API server
python -m uvicorn src.api.main:app --reload --port 8000
```

### Access API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/api/health
- **Metrics**: http://localhost:8000/api/metrics

## API Endpoints

### Chat
- `POST /api/chat` - Ask questions and get AI-powered answers

### Documents
- `POST /api/documents/upload` - Upload documents (PDF, DOCX, TXT)
- `GET /api/documents` - List all documents
- `POST /api/documents/reset` - Reset database (delete all documents)

### Monitoring
- `GET /api/health` - Service health check
- `GET /api/metrics` - Performance metrics

## Example Usage

### Chat Request

```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"question": "What was the total revenue in Q4 2025?"}'
```

### Upload Document

```bash
curl -X POST "http://localhost:8000/api/documents/upload" \
  -F "file=@sales_report.pdf"
```

### Health Check

```bash
curl http://localhost:8000/api/health
```

## Architecture

```
src/api/
├── main.py          # FastAPI application
├── routes/          # API endpoints
│   ├── chat.py      # Chat endpoints
│   ├── documents.py # Document management
│   └── health.py    # Health & metrics
└── models/          # Pydantic schemas
    └── schemas.py   # Request/Response models
```

## Production Deployment

### Using Docker

```bash
# Build and run with docker-compose
docker-compose up -d

# API will be available at http://localhost:8000
```

### Using Gunicorn (Production Server)

```bash
gunicorn src.api.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

## Development

### Testing

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest tests/api/
```

### Auto-reload on code changes

```bash
uvicorn src.api.main:app --reload
```

## Security

- CORS is currently configured to allow all origins (`*`)
- **For production**: Update `allow_origins` in `main.py` to specific domains
- Add authentication middleware for protected endpoints
- Use HTTPS in production

## Environment Variables

Create a `.env` file:

```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=tinyllama
VECTOR_STORE_PATH=./data/vector_store/chroma_db
LOG_LEVEL=INFO
```

## Performance

- Average response time: ~1-3 seconds (with TinyLlama)
- Concurrent requests: Supported via async/await
- Max upload size: 10MB (configurable)

## Notes

- API runs on port 8000 (Streamlit UI on port 8501)
- Both can run simultaneously
- Shared vector database and RAG engine
- Auto-generated API docs via FastAPI
