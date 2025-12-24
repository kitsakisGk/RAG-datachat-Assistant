# Quick Start Guide

## Prerequisites

- Python 3.10 or higher
- Git
- 8GB+ RAM recommended
- Ollama (for local LLM)

## Installation Steps

### 1. Clone or Navigate to Project

You're already here! The folder should be renamed to `RAG-datachat-Assistant`.

### 2. Set Up Virtual Environment

**On Windows:**
```bash
# Run the setup script
setup.bat

# Or manually:
py -m venv venv
venv\Scripts\activate
```

**On Linux/Mac:**
```bash
# Run the setup script
bash setup.sh

# Or manually:
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will install:
- LangChain for RAG orchestration
- ChromaDB for vector storage
- Streamlit for UI
- Ollama client for LLM
- And all other dependencies

### 4. Install Ollama

**Download Ollama:**
- Visit [https://ollama.ai](https://ollama.ai)
- Download for your OS (Windows/Mac/Linux)
- Install and start Ollama

**Pull the Mistral model:**
```bash
ollama pull mistral
```

**Verify installation:**
```bash
ollama list
```

You should see `mistral` in the list.

### 5. Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your settings (optional for now)
```

### 6. Run the Application

```bash
streamlit run src/ui/app.py
```

The app will open in your browser at `http://localhost:8501`

## First Steps

1. **Upload a document**: Start with a simple text file or PDF
2. **Ask a question**: Try "What is this document about?"
3. **Connect a database**: Add your database credentials in settings
4. **Query your data**: Ask "Show me the top 10 customers"

## Development Workflow

### Run Tests
```bash
pytest tests/
```

### Format Code
```bash
black src/
```

### Type Checking
```bash
mypy src/
```

### Run API Server (FastAPI)
```bash
uvicorn src.api.main:app --reload
```

## Troubleshooting

### Ollama Connection Issues
- Make sure Ollama is running: `ollama serve`
- Check the URL in `.env`: `OLLAMA_BASE_URL=http://localhost:11434`

### Vector Store Issues
- Delete and recreate: `rm -rf data/vector_store/chroma_db`
- The app will recreate it on next run

### Import Errors
- Make sure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

### Port Already in Use
- Streamlit: Change port with `streamlit run src/ui/app.py --server.port 8502`
- FastAPI: Change port in `config/settings.py`

## What's Next?

Check out the [Architecture Documentation](architecture.md) to understand how everything works!

## Week 1 Goals

- [ ] Set up development environment
- [ ] Get basic RAG working with document upload
- [ ] Create simple chat interface
- [ ] Test with sample documents
- [ ] Commit progress to git

Happy coding! 🚀
