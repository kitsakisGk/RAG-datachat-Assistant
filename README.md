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
- **LLM**: Ollama (Mistral/Llama) + OpenAI (optional)
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
git clone https://github.com/yourusername/RAG-datachat-Assistant.git
cd RAG-datachat-Assistant

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Ollama and pull model
ollama pull mistral

# Run the application
streamlit run src/ui/app.py
```

### Docker Deployment

```bash
docker-compose up -d
```

## 📚 Documentation

- [Architecture Overview](docs/architecture.md)
- [API Documentation](docs/api.md)
- [Development Guide](docs/development.md)
- [Deployment Guide](docs/deployment.md)

## ✨ Current Features

### Implemented ✅
- [x] RAG pipeline with semantic search
- [x] ChromaDB vector database
- [x] Ollama LLM integration
- [x] Document upload (PDF, DOCX, TXT)
- [x] Streamlit chat interface
- [x] Conversation memory
- [x] Source attribution

### In Development 🚧
- [ ] Database connectors (PostgreSQL, MySQL, SQLite)
- [ ] Natural language to SQL generation
- [ ] CSV/Excel file analysis
- [ ] Auto-visualization
- [ ] Data insights generation

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) first.

## 📄 License

MIT License - see [LICENSE](LICENSE) for details

## 🙏 Acknowledgments

- Built with [LangChain](https://langchain.com)
- Powered by [Ollama](https://ollama.ai)
- UI with [Streamlit](https://streamlit.io)

## 📧 Contact

- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your Name](https://linkedin.com/in/yourprofile)
- Email: your.email@example.com

---

**⭐ Star this repo if you find it helpful!**

Built with ❤️ for data analysts everywhere
