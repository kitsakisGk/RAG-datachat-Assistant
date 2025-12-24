"""
Basic tests for RAG engine functionality
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.rag_engine import RAGEngine
from src.core.vector_store import VectorStore
from src.embeddings.embeddings import get_embedding_generator


def test_embedding_generator():
    """Test embedding generation"""
    print("Testing embedding generator...")

    embedder = get_embedding_generator()
    embedder.load_model()

    text = "This is a test document about data analysis."
    embedding = embedder.generate_embedding(text)

    assert len(embedding) == embedder.get_dimension()
    print(f"✓ Embedding generated successfully (dimension: {len(embedding)})")


def test_vector_store():
    """Test vector store operations"""
    print("\nTesting vector store...")

    # Create test vector store
    vector_store = VectorStore(collection_name="test_collection")

    # Add test documents
    documents = [
        "Python is a programming language used for data analysis.",
        "Machine learning models can predict future trends.",
        "SQL is used to query databases."
    ]

    metadatas = [
        {"source": "doc1", "topic": "programming"},
        {"source": "doc2", "topic": "ml"},
        {"source": "doc3", "topic": "databases"}
    ]

    ids = vector_store.add_documents(documents, metadatas)
    print(f"✓ Added {len(ids)} documents")

    # Test search
    results = vector_store.search("What is Python?", n_results=2)
    assert len(results["documents"]) > 0
    print(f"✓ Search returned {len(results['documents'])} results")

    # Test count
    count = vector_store.count()
    print(f"✓ Vector store contains {count} documents")

    # Clean up
    vector_store.reset()
    print("✓ Vector store reset")


def test_rag_engine():
    """Test RAG engine end-to-end"""
    print("\nTesting RAG engine...")

    # Create RAG engine
    rag_engine = RAGEngine(
        llm_model="mistral",
        top_k=3
    )

    # Add knowledge
    documents = [
        "The capital of France is Paris. Paris is known for the Eiffel Tower.",
        "Python was created by Guido van Rossum in 1991.",
        "Machine learning is a subset of artificial intelligence.",
        "The Great Wall of China is over 13,000 miles long."
    ]

    rag_engine.add_documents(documents)
    print(f"✓ Added {len(documents)} documents to knowledge base")

    # Test query (without actually calling LLM)
    print("\nNote: Actual LLM testing requires Ollama to be running.")
    print("Testing retrieval only...")

    question = "What is the capital of France?"
    context = rag_engine.retrieve_context(question, n_results=2)

    assert len(context["documents"]) > 0
    print(f"✓ Retrieved {len(context['documents'])} relevant documents")
    print(f"  First result: {context['documents'][0][:100]}...")

    # Get stats
    stats = rag_engine.get_stats()
    print(f"✓ RAG engine stats: {stats}")

    # Clean up
    rag_engine.vector_store.reset()
    print("✓ Cleaned up test data")


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("RAG DataChat Assistant - Component Tests")
    print("=" * 60)

    try:
        test_embedding_generator()
        test_vector_store()
        test_rag_engine()

        print("\n" + "=" * 60)
        print("✅ All tests passed!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_tests()
