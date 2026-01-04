# 📁 Project Structure

```
RAG-datachat-Assistant/
│
├── 📄 README.md                 # Main project documentation
├── 📄 LICENSE                   # MIT License
├── 📄 CONTRIBUTING.md           # Contribution guidelines
├── 📄 requirements.txt          # Python dependencies
├── 📄 .env.example              # Environment variables template
├── 📄 .gitignore                # Git ignore rules
│
├── 🐳 Dockerfile                # Docker container definition
├── 🐳 docker-compose.yml        # Multi-container orchestration
├── 🐳 .dockerignore             # Docker build exclusions
│
├── 🔧 setup.sh                  # Linux/Mac setup script
├── 🔧 setup.bat                 # Windows setup script
│
├── 📚 docs/                     # Documentation
│   ├── QUICKSTART.md            # 5-minute getting started guide
│   ├── DEPLOY.md                # Production deployment guide
│   ├── PROJECT_STATUS.md        # Development roadmap
│   └── architecture.md          # System architecture details
│
├── 📸 screenshots/              # UI screenshots for README
│   └── README.md                # Screenshot placeholder
│
├── ⚙️  config/                   # Configuration files
│   └── settings.py              # Application settings
│
├── 💾 data/                     # Data storage
│   ├── raw/                     # Raw uploaded documents
│   ├── processed/               # Processed documents
│   ├── vector_store/            # ChromaDB storage
│   │   └── chroma_db/           # Vector embeddings
│   ├── sample_sales_data.txt    # Sample data for testing
│   └── product_documentation.txt # Sample product docs
│
├── 📝 logs/                     # Application logs
│   └── app_YYYY-MM-DD.log       # Daily rotating logs
│
├── 🧪 tests/                    # Test suite
│   └── test_rag_engine.py       # RAG engine tests
│
├── 📓 notebooks/                # Jupyter notebooks for experiments
│
├── 💻 src/                      # Source code
│   │
│   ├── 🎨 ui/                   # User interface
│   │   └── app.py               # Streamlit web app
│   │
│   ├── 🧠 core/                 # Core RAG components
│   │   ├── rag_engine.py        # Main RAG orchestration
│   │   └── vector_store.py      # Vector database interface
│   │
│   ├── 🤖 llm/                  # LLM integration
│   │   ├── ollama_client.py     # Ollama API client
│   │   └── prompt_templates.py  # Prompt engineering templates
│   │
│   ├── 📊 embeddings/           # Text embedding generation
│   │   └── embeddings.py        # Sentence transformer wrapper
│   │
│   ├── 🔌 connectors/           # Data connectors
│   │   └── document_loader.py   # Document parsing (PDF, DOCX, TXT)
│   │
│   └── 🛠️  utils/               # Utility modules
│       ├── logger.py            # Logging configuration
│       └── validators.py        # Input validation
│
└── 🐍 venv/                     # Python virtual environment (local only)
└── 🤖 ollama_models/            # Ollama model storage (local only)
```

## 📦 Key Components

### Core Application
- **src/core/rag_engine.py** - Main RAG pipeline orchestration
- **src/core/vector_store.py** - ChromaDB vector database management
- **src/llm/ollama_client.py** - Local LLM inference with Ollama

### User Interface
- **src/ui/app.py** - Streamlit web interface with chat functionality

### Data Processing
- **src/connectors/document_loader.py** - Document parsing and chunking
- **src/embeddings/embeddings.py** - Text-to-vector conversion

### Configuration
- **config/settings.py** - Centralized application settings
- **.env.example** - Environment variables template

## 🚀 Deployment Files

- **Dockerfile** - Production-ready container image
- **docker-compose.yml** - One-command deployment with Ollama
- **.dockerignore** - Optimized Docker builds

## 📚 Documentation

- **docs/QUICKSTART.md** - Get started in 5 minutes
- **docs/DEPLOY.md** - Production deployment guide
- **docs/architecture.md** - Detailed system architecture
- **docs/PROJECT_STATUS.md** - Development roadmap

## 🧪 Development

- **tests/** - Unit and integration tests
- **notebooks/** - Jupyter notebooks for experimentation
- **setup.sh/bat** - Automated environment setup

## 📊 Data Flow

```
User Upload → Document Loader → Chunker → Embeddings → Vector Store
                                                              ↓
User Question → Embeddings → Vector Search → Context → LLM → Answer
```

## 🔒 Ignored Files (not in git)

- `venv/` - Virtual environment
- `ollama_models/` - LLM model files (~4GB)
- `data/vector_store/` - Vector database
- `logs/` - Application logs
- `.env` - Environment secrets
- `__pycache__/` - Python cache

## 📝 Notes

- All configuration is centralized in `config/settings.py`
- Logs rotate daily and are kept for 30 days
- Vector store persists across restarts in `data/vector_store/`
- Sample data provided in `data/` for testing
