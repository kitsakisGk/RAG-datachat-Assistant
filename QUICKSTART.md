## 🚀 Quick Start - Get Running in 5 Minutes

### Prerequisites Check

Before starting, ensure you have:
- ✅ Python 3.10+ installed
- ✅ 8GB+ RAM
- ✅ Internet connection (for downloading models)

### Step 1: Rename Project Folder

Rename the folder from `Project_RAG` to `RAG-datachat-Assistant`

### Step 2: Set Up Virtual Environment

**Windows:**
```bash
py -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will take a few minutes. Go grab a coffee! ☕

### Step 4: Install Ollama

**Download Ollama:**
1. Visit: https://ollama.ai
2. Download for your OS (Windows/Mac/Linux)
3. Install and run Ollama

**Pull the Mistral model:**
```bash
ollama pull mistral
```

**Verify installation:**
```bash
ollama list
```

You should see `mistral` in the list.

### Step 5: Test the Components

Run the test script to ensure everything works:

```bash
python tests/test_rag_engine.py
```

Expected output:
```
==================================================
RAG DataChat Assistant - Component Tests
==================================================
Testing embedding generator...
✓ Embedding generated successfully (dimension: 768)

Testing vector store...
✓ Added 3 documents
✓ Search returned 1 results
✓ Vector store contains 3 documents
✓ Vector store reset

Testing RAG engine...
✓ Added 4 documents to knowledge base
✓ Retrieved 2 relevant documents
✓ RAG engine stats: {...}
✓ Cleaned up test data

==================================================
✅ All tests passed!
==================================================
```

### Step 6: Run the Application

Start the Streamlit UI:

```bash
streamlit run src/ui/app.py
```

The app will open in your browser at `http://localhost:8501`

### Step 7: Try It Out!

1. Click **"Initialize System"** in the sidebar
2. Upload a document (try a .txt or .pdf file)
3. Click **"Load Documents"**
4. Ask a question in the chat: "What is this document about?"
5. Watch the magic happen! ✨

## 📝 Example Documents to Try

Create a test file `test_document.txt`:

```
# Python Programming

Python is a high-level programming language created by Guido van Rossum in 1991.

It is known for its simple syntax and readability. Python is widely used in:
- Data science and machine learning
- Web development
- Automation and scripting
- Scientific computing

Popular Python libraries include NumPy, Pandas, Matplotlib, and TensorFlow.
```

Upload this and ask questions like:
- "Who created Python?"
- "What is Python used for?"
- "What are some popular Python libraries?"

## 🐛 Troubleshooting

### Ollama Connection Error
```
Error: Ollama service is not available
```
**Fix:** Make sure Ollama is running:
```bash
ollama serve
```

### Port Already in Use
```
Error: Address already in use
```
**Fix:** Run Streamlit on a different port:
```bash
streamlit run src/ui/app.py --server.port 8502
```

### Import Errors
```
ModuleNotFoundError: No module named 'sentence_transformers'
```
**Fix:** Reinstall dependencies:
```bash
pip install -r requirements.txt --force-reinstall
```

### ChromaDB Issues
```
Error: Cannot connect to ChromaDB
```
**Fix:** Delete and recreate the vector store:
```bash
rm -rf data/vector_store/chroma_db  # Linux/Mac
rmdir /s data\vector_store\chroma_db  # Windows
```

## 📊 What We Built

You now have a working RAG system with:

✅ **Vector Store** - ChromaDB for semantic search
✅ **Embeddings** - BGE model for text vectors
✅ **LLM Integration** - Ollama with Mistral
✅ **Document Loading** - PDF, DOCX, TXT support
✅ **Chat UI** - Streamlit interface
✅ **Conversation Memory** - Context-aware responses

## 🎯 Next Steps

- Add more documents to test different scenarios
- Try different types of questions
- Experiment with the chunk size (in settings.py)
- Look at the logs in the `logs/` folder

## 🎉 You're All Set!

Your RAG DataChat Assistant is now running!

Check [README.md](README.md) for full documentation.
Check [docs/architecture.md](docs/architecture.md) to understand how it works.

Happy chatting with your data! 🤖
