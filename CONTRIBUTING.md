# Contributing to RAG DataChat Assistant

Thank you for your interest in contributing! This project is designed to help data analysts work with their data using natural language.

## Development Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and configure
5. Install Ollama and pull the model:
   ```bash
   ollama pull mistral
   ```

## Project Structure

- `src/core/` - Core RAG engine
- `src/llm/` - LLM integrations
- `src/connectors/` - Database and file connectors
- `src/api/` - FastAPI backend
- `src/ui/` - Streamlit frontend
- `docs/` - Documentation
- `tests/` - Test suite

## Coding Standards

- Follow PEP 8 style guide
- Use type hints
- Write docstrings for all functions
- Keep functions small and focused
- Write tests for new features

## Running Tests

```bash
pytest tests/
```

## Submitting Changes

1. Create a new branch for your feature
2. Make your changes
3. Write/update tests
4. Run tests to ensure they pass
5. Submit a pull request

## Code Review Process

All submissions require review. We'll review your PR and may suggest changes.

## Questions?

Open an issue or start a discussion!
