# 🏗️ Architecture Overview

## System Architecture

The RAG DataChat Assistant follows a layered architecture designed for modularity, scalability, and maintainability.

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE LAYER                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Streamlit   │  │   REST API   │  │  CLI Tools   │      │
│  │     UI       │  │   Endpoints  │  │              │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                   QUERY PROCESSING LAYER                     │
│  ┌────────────────────────────────────────────────────┐     │
│  │  Intent Classification & Entity Recognition        │     │
│  └────────────────────────────────────────────────────┘     │
│  ┌────────────────────────────────────────────────────┐     │
│  │  Query Parsing & Business Term Mapping             │     │
│  └────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                   RAG RETRIEVAL LAYER                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Vector     │  │   Semantic   │  │   Context    │      │
│  │   Search     │  │   Ranking    │  │   Assembly   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                              │
│  ┌────────────────────────────────────────────────────┐     │
│  │        Vector Database (ChromaDB/Qdrant)           │     │
│  │  • Schema metadata  • Past queries  • Docs         │     │
│  └────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    GENERATION LAYER                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │     SQL      │  │    Python    │  │ Explanation  │      │
│  │  Generation  │  │    Code      │  │  Generator   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                              │
│  ┌────────────────────────────────────────────────────┐     │
│  │          LLM Engine (Ollama/OpenAI)                │     │
│  │  • Mistral  • Llama  • GPT-4 (optional)            │     │
│  └────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    EXECUTION LAYER                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   SQL        │  │   Python     │  │   Result     │      │
│  │   Executor   │  │   Sandbox    │  │   Cache      │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    DATA SOURCE LAYER                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Databases   │  │    Files     │  │     APIs     │      │
│  │  (SQL/NoSQL) │  │  (CSV/Excel) │  │    (REST)    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                  PRESENTATION LAYER                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Visualization│  │   Insights   │  │   Export     │      │
│  │   Engine     │  │  Generator   │  │   (PDF/XLS)  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Query Understanding
- **Intent Classifier**: Determines if query needs SQL, analysis, or visualization
- **Entity Recognizer**: Extracts entities (tables, columns, metrics, time periods)
- **Business Term Mapper**: Maps colloquial terms to database schema

### 2. RAG Engine
- **Vector Store**: Stores embeddings of schemas, queries, and documentation
- **Retrieval System**: Semantic search for relevant context
- **Ranking Algorithm**: Prioritizes most relevant context
- **Context Assembly**: Builds comprehensive context for LLM

### 3. Generation System
- **Prompt Builder**: Constructs optimized prompts with context
- **SQL Generator**: Produces valid SQL with schema awareness
- **Code Generator**: Creates Python analysis scripts
- **Validator**: Checks generated code for safety and correctness

### 4. Execution Engine
- **SQL Executor**: Runs queries with timeout and row limits
- **Sandbox**: Isolated Python environment for code execution
- **Cache Manager**: Stores results for repeated queries
- **Error Handler**: Graceful error handling and retry logic

### 5. Data Connectors
- **Database Adapters**: Universal interface for all DB types
- **File Parsers**: Handles CSV, Excel, JSON, Parquet
- **API Client**: Generic REST API connector
- **Schema Extractor**: Automatic metadata discovery

## Data Flow

### Query Processing Flow

```
User Query: "Show me top 10 customers by revenue last quarter"
                    ↓
1. PARSE INTENT
   → Type: SQL Query
   → Entities: {metric: "revenue", entity: "customers",
                 count: 10, period: "last quarter"}
                    ↓
2. RETRIEVE CONTEXT
   → Vector search for "customers" and "revenue"
   → Found: customers table, orders table, revenue column
   → Retrieved: Schema + Past queries + Documentation
                    ↓
3. GENERATE SQL
   Prompt: "Given schema: [context], generate SQL for..."
   LLM Output:
   ```sql
   SELECT c.customer_name, SUM(o.total) as revenue
   FROM customers c
   JOIN orders o ON c.id = o.customer_id
   WHERE o.order_date >= DATE_TRUNC('quarter', CURRENT_DATE - INTERVAL '3 months')
     AND o.order_date < DATE_TRUNC('quarter', CURRENT_DATE)
   GROUP BY c.customer_name
   ORDER BY revenue DESC
   LIMIT 10;
   ```
                    ↓
4. VALIDATE & EXECUTE
   → Syntax check: ✓
   → Security check: ✓ (read-only, no DROP/DELETE)
   → Execute with timeout: 30s
   → Results: 10 rows returned
                    ↓
5. VISUALIZE & EXPLAIN
   → Auto-select chart: Bar chart (categorical + numeric)
   → Generate insight: "Top customer is Acme Corp with $1.2M"
   → Create explanation: "I analyzed Q3 2024 orders..."
                    ↓
6. PRESENT
   → Display table
   → Show chart
   → Provide explanation
   → Offer export options
```

## Technology Stack Details

### Vector Database
- **Development**: ChromaDB (lightweight, easy setup)
- **Production**: Qdrant (scalable, high performance)
- **Embedding Model**: BGE-M3 or E5-Large (multilingual support)

### LLM Options
1. **Local (Privacy-First)**
   - Ollama with Mistral 7B or Llama 2
   - No data leaves the system
   - Lower cost

2. **Cloud (Higher Accuracy)**
   - OpenAI GPT-4
   - Better complex query handling
   - Pay per use

### Database Support
- **SQL Databases**: PostgreSQL, MySQL, SQLite, SQL Server
- **Cloud Warehouses**: Snowflake, BigQuery, Redshift
- **Interface**: SQLAlchemy for universal compatibility

### Caching Strategy
- **Query Cache**: Redis for fast repeated queries
- **Result Cache**: Local storage with TTL
- **Embedding Cache**: Persistent vector store

## Security Architecture

### Query Safety
1. **Read-Only Mode**: Default connection is read-only
2. **Query Whitelist**: Only SELECT statements allowed
3. **Row Limits**: Maximum 10,000 rows per query
4. **Timeout**: 30-second query timeout
5. **Sanitization**: SQL injection prevention

### Data Isolation
- **Multi-Tenancy**: Separate vector stores per user
- **Credential Encryption**: Database passwords encrypted
- **Audit Logging**: All queries logged
- **No Data Persistence**: Results not stored permanently

### Code Execution
- **Sandboxed Environment**: Isolated Python execution
- **Resource Limits**: CPU, memory, time constraints
- **Import Restrictions**: Only whitelisted libraries
- **File System Access**: Read-only access to data

## Scalability Design

### Horizontal Scaling
- **Stateless API**: Can run multiple instances
- **Load Balancer**: Distribute requests
- **Async Processing**: Celery for long queries
- **Queue System**: Redis-based task queue

### Performance Optimization
- **Connection Pooling**: Reuse database connections
- **Batch Processing**: Process multiple queries together
- **Streaming Results**: Don't load all data in memory
- **Lazy Loading**: Load data only when needed

### Monitoring
- **Metrics**: Prometheus for system metrics
- **Logging**: Structured logging with Loguru
- **Tracing**: Request tracing for debugging
- **Alerts**: Error rate, latency, resource usage

## Development Phases

### Phase 1: Foundation ✅
- Basic RAG pipeline
- ChromaDB integration
- Ollama LLM setup
- Simple Streamlit UI

### Phase 2: Data Connectivity 🚧
- Database connectors
- File upload handling
- Schema extraction
- Unified data catalog

### Phase 3: Intelligence 📅
- Complex SQL generation
- Auto-analysis features
- Smart visualizations
- Business term mapping

### Phase 4: Production 📅
- Docker deployment
- Security hardening
- Performance tuning
- Monitoring setup

## File Organization

```
src/
├── core/
│   ├── rag_engine.py          # Main RAG logic
│   ├── embeddings.py           # Embedding generation
│   ├── retrieval.py            # Context retrieval
│   └── cache.py                # Caching layer
├── llm/
│   ├── ollama_client.py        # Ollama integration
│   ├── openai_client.py        # OpenAI integration
│   ├── prompt_templates.py     # Prompt management
│   └── generator.py            # SQL/Code generation
├── connectors/
│   ├── database.py             # DB connectors
│   ├── file_parser.py          # File handling
│   ├── api_client.py           # API integration
│   └── schema_extractor.py     # Metadata extraction
├── api/
│   ├── main.py                 # FastAPI app
│   ├── routes.py               # API endpoints
│   ├── models.py               # Pydantic models
│   └── middleware.py           # Auth, logging
├── ui/
│   ├── app.py                  # Streamlit app
│   ├── components/             # UI components
│   └── utils.py                # UI helpers
└── utils/
    ├── validators.py           # Input validation
    ├── formatters.py           # Output formatting
    └── logger.py               # Logging setup
```

## Design Principles

1. **Modularity**: Each component is independent and replaceable
2. **Security First**: Safe by default, explicit permissions
3. **Performance**: Cache everything, optimize early
4. **User Experience**: Fast feedback, clear explanations
5. **Maintainability**: Clean code, comprehensive tests
6. **Scalability**: Designed to grow from 1 to 1000 users

## Future Enhancements

- Multi-user collaboration
- Advanced analytics (ML predictions)
- Natural language report generation
- Integration with BI tools (Tableau, Power BI)
- Voice interface
- Mobile app
