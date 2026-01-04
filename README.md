# 🤖 RAG DataChat Assistant

> "Talk to your data like you talk to a colleague"

A production-ready RAG (Retrieval-Augmented Generation) system that enables natural language data analysis across databases, files, and APIs.

## 🎯 What is this?

DataChat AI is an intelligent assistant that understands your data context and lets you analyze it using plain English - no SQL or Python knowledge required.

**Ask questions like:**
- "Show me top customers by revenue last quarter"
- "Compare sales growth YoY for top 5 products"
- "What's causing the spike in churn rate?"

**Get:**
- Accurate SQL queries generated automatically
- Beautiful visualizations
- Plain English insights and explanations
- Exportable reports (PDF, Excel, Jupyter notebooks)

## 🚀 Key Features

- **Multi-Source Support**: PostgreSQL, MySQL, SQLite, Snowflake, BigQuery, CSV, Excel, APIs
- **Intelligent Query Understanding**: Handles complex JOINs, time-based queries, business terminology
- **Auto-Analysis**: Automated exploratory data analysis, statistical tests, anomaly detection
- **Smart Visualizations**: Automatic chart type selection based on data
- **Privacy-First**: Local LLM option (Ollama) for sensitive data
- **Production-Ready**: Docker deployment, security, caching, monitoring

## 🏗️ Architecture

```
User Query → Understanding Layer → Context Retrieval → Generation → Execution → Presentation
```

### Tech Stack

- **Vector DB**: ChromaDB (dev) → Qdrant (production)
- **LLM**: Ollama (TinyLlama/Mistral/Llama) + OpenAI (optional)
- **Embeddings**: BGE-M3 / E5-Large
- **Backend**: FastAPI
- **Frontend**: Streamlit → Next.js
- **SQL Engine**: SQLAlchemy + DuckDB
- **Deployment**: Docker + Railway/Fly.io

## 📦 Project Structure

```
RAG-datachat-Assistant/
├── src/
│   ├── core/           # Core RAG engine
│   ├── api/            # FastAPI backend
│   ├── ui/             # Streamlit frontend
│   ├── connectors/     # Database & file connectors
│   ├── embeddings/     # Vector embeddings
│   ├── llm/            # LLM integration
│   └── utils/          # Utilities
├── data/
│   ├── raw/            # Raw data files
│   ├── processed/      # Processed data
│   └── vector_store/   # Vector database storage
├── docs/               # Documentation
├── tests/              # Test suite
├── config/             # Configuration files
├── notebooks/          # Jupyter notebooks for experiments
└── docker/             # Docker configurations

```

## 🛠️ Quick Start

### Prerequisites

- Python 3.10+
- Docker (optional, for containerized deployment)
- Ollama (for local LLM)

### Installation

```bash
# Clone the repository
git clone https://github.com/kitsakisGk/RAG-datachat-Assistant.git
cd RAG-datachat-Assistant

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Ollama and pull model (TinyLlama is fast and lightweight)
ollama pull tinyllama

# Run the application
streamlit run src/ui/app.py
```

### Docker Deployment

```bash
docker-compose up -d
```

## 📚 Documentation

- [Quick Start Guide](docs/QUICKSTART.md) - Get started in 5 minutes
- [Deployment Guide](docs/DEPLOY.md) - Deploy to production with Docker
- [Architecture Overview](docs/architecture.md) - System design and components
- [Project Status](docs/PROJECT_STATUS.md) - Development roadmap and progress

## ✨ Features

- **RAG Pipeline** - Semantic search with retrieval-augmented generation
- **Vector Database** - ChromaDB for efficient document storage and retrieval
- **LLM Integration** - Local inference with Ollama (TinyLlama/Mistral/Llama)
- **Document Processing** - Support for PDF, DOCX, and TXT files
- **Chat Interface** - Interactive Streamlit UI with conversation memory
- **Source Attribution** - Track and display source documents for answers
- **Privacy-First** - All data processing happens locally

## 📸 Screenshots

### Main Chat Interface
![Chat Interface](screenshots/chat-interface.png)
*Ask questions in natural language and get AI-powered answers from your documents*

### Document Upload
![Document Upload](screenshots/document-upload.png)
*Upload PDF, DOCX, or TXT files to your knowledge base*

### Sample Q&A
![Sample Q&A](screenshots/sample-qa.png)
*Example: Asking about Q4 2025 sales data and getting detailed insights*

> **Note**: Add your screenshots to the `screenshots/` folder and they'll appear here!

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) first.

## 📄 License

MIT License - see [LICENSE](LICENSE) for details

## 🙏 Acknowledgments

- Built with [LangChain](https://langchain.com)
- Powered by [Ollama](https://ollama.ai)
- UI with [Streamlit](https://streamlit.io)

## 📧 Contact

- GitHub: [@kitsakisGk](https://github.com/kitsakisGk)
- LinkedIn: [Georgios Kitsakis](https://www.linkedin.com/in/georgios-kitsakis-gr/)
- Email: kitsakisgk@gmail.com

---

**⭐ Star this repo if you find it helpful!**
