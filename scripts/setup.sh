#!/bin/bash

# RAG DataChat Assistant - Setup Script
echo "🚀 Setting up RAG DataChat Assistant..."

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv || py -m venv venv

# Activate virtual environment
echo "✅ Virtual environment created!"
echo ""
echo "To activate the virtual environment, run:"
echo "  On Linux/Mac:  source venv/bin/activate"
echo "  On Windows:    venv\\Scripts\\activate"
echo ""
echo "After activation, run:"
echo "  pip install -r requirements.txt"
echo ""
echo "To install Ollama and pull the model:"
echo "  1. Install Ollama from https://ollama.ai"
echo "  2. Run: ollama pull mistral"
echo ""
echo "Then start the app:"
echo "  streamlit run src/ui/app.py"
