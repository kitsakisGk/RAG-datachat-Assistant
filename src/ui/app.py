"""
Streamlit UI for RAG DataChat Assistant
"""
import streamlit as st
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.core.rag_engine import RAGEngine
from src.core.vector_store import VectorStore
from src.connectors.document_loader import DocumentLoader
from src.utils.logger import get_logger

logger = get_logger(__name__)

# Page configuration
st.set_page_config(
    page_title="RAG DataChat Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .source-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state
def init_session_state():
    """Initialize Streamlit session state"""
    if 'rag_engine' not in st.session_state:
        st.session_state.rag_engine = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'documents_loaded' not in st.session_state:
        st.session_state.documents_loaded = False


def initialize_rag_engine():
    """Initialize RAG engine"""
    if st.session_state.rag_engine is None:
        try:
            with st.spinner("Initializing RAG engine..."):
                vector_store = VectorStore()
                st.session_state.rag_engine = RAGEngine(
                    vector_store=vector_store,
                    llm_model="mistral",
                    top_k=5
                )
            logger.info("RAG engine initialized successfully")
            return True
        except Exception as e:
            st.error(f"Failed to initialize RAG engine: {e}")
            logger.error(f"RAG initialization error: {e}")
            return False
    return True


def main():
    """Main application"""
    init_session_state()

    # Header
    st.markdown('<div class="main-header">🤖 RAG DataChat Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Talk to your data like you talk to a colleague</div>', unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")

        # Initialize button
        if st.button("🚀 Initialize System", type="primary", use_container_width=True):
            if initialize_rag_engine():
                st.success("System initialized!")

        st.divider()

        # Document upload section
        st.header("📄 Upload Documents")

        uploaded_files = st.file_uploader(
            "Choose files",
            type=['txt', 'pdf', 'docx', 'md'],
            accept_multiple_files=True,
            help="Upload documents to add to the knowledge base"
        )

        if uploaded_files and st.button("📥 Load Documents", use_container_width=True):
            if st.session_state.rag_engine is None:
                st.error("Please initialize the system first!")
            else:
                load_documents(uploaded_files)

        st.divider()

        # System stats
        if st.session_state.rag_engine:
            st.header("📊 System Stats")
            stats = st.session_state.rag_engine.get_stats()
            st.metric("Total Documents", stats['total_documents'])
            st.metric("Conversation Length", stats['conversation_length'])

            if st.button("🗑️ Clear History", use_container_width=True):
                st.session_state.rag_engine.clear_history()
                st.session_state.chat_history = []
                st.success("History cleared!")
                st.rebalance()

    # Main content area
    if st.session_state.rag_engine is None:
        # Welcome screen
        st.info("👈 Click **Initialize System** in the sidebar to get started!")

        st.subheader("🎯 What can I do?")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            **📚 Document Analysis**
            - Upload PDFs, Word docs, text files
            - Ask questions about your documents
            - Get AI-powered answers with sources

            **💡 Smart Features**
            - Semantic search across documents
            - Context-aware responses
            - Conversation memory
            """)

        with col2:
            st.markdown("""
            **🔮 Coming Soon**
            - Database connectivity
            - Natural language to SQL
            - Auto-visualization
            - Data insights generation

            **🚀 Quick Start**
            1. Initialize the system
            2. Upload your documents
            3. Start asking questions!
            """)

    else:
        # Chat interface
        st.subheader("💬 Chat")

        # Display chat history
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.write(message["content"])
                if "sources" in message:
                    with st.expander("📚 View Sources"):
                        st.write(f"Retrieved from {message['sources']} documents")

        # Chat input
        if prompt := st.chat_input("Ask a question about your data..."):
            # Add user message
            st.session_state.chat_history.append({"role": "user", "content": prompt})

            with st.chat_message("user"):
                st.write(prompt)

            # Generate response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        response = st.session_state.rag_engine.chat(
                            question=prompt,
                            use_history=True,
                            return_context=True
                        )

                        answer = response["answer"]
                        num_sources = response["num_sources"]

                        st.write(answer)

                        # Add assistant message
                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": answer,
                            "sources": num_sources
                        })

                        # Show sources
                        if num_sources > 0:
                            with st.expander("📚 View Sources"):
                                st.write(f"Answer generated using {num_sources} relevant documents")
                                if "context" in response:
                                    for i, doc in enumerate(response["context"]["documents"]):
                                        st.markdown(f"**Source {i+1}:**")
                                        st.text(doc[:200] + "..." if len(doc) > 200 else doc)

                    except Exception as e:
                        error_msg = f"Error generating response: {str(e)}"
                        st.error(error_msg)
                        logger.error(error_msg)


def load_documents(uploaded_files):
    """Load uploaded documents into the knowledge base"""
    try:
        with st.spinner(f"Loading {len(uploaded_files)} documents..."):
            loader = DocumentLoader(chunk_size=1000, chunk_overlap=200)

            # Save uploaded files temporarily
            import tempfile
            import os

            temp_files = []
            for uploaded_file in uploaded_files:
                # Create temp file
                with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    temp_files.append(tmp_file.name)

            # Load documents
            doc_data = loader.load_multiple_documents(temp_files)

            # Add to RAG engine
            st.session_state.rag_engine.add_documents(
                documents=doc_data["chunks"],
                metadatas=doc_data["metadatas"]
            )

            # Clean up temp files
            for temp_file in temp_files:
                os.unlink(temp_file)

            st.success(f"✅ Loaded {doc_data['num_documents']} documents ({doc_data['total_chunks']} chunks)")
            st.session_state.documents_loaded = True
            logger.info(f"Loaded {doc_data['num_documents']} documents with {doc_data['total_chunks']} chunks")

    except Exception as e:
        st.error(f"Failed to load documents: {e}")
        logger.error(f"Document loading error: {e}")


if __name__ == "__main__":
    main()
