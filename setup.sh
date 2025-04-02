#!/bin/bash

#!/bin/bash

echo "🚀 TravelBot Setup Script"

# Create folders early
mkdir -p rag/jtr_chunks models web/templates

# Create virtual environment
python3 -m venv .venv

echo "💡 Virtual environment created. To activate manually:"
echo "source .venv/bin/activate"

# Activate virtual environment
. .venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
pip install torch
pip install accelerate

# Ensure critical packages are installed (in case requirements.txt misses them)
pip install -U langchain-community transformers torch sentence-transformers faiss-cpu

# Auto-build embeddings if chunk files exist
echo "🧠 Building semantic index..."
python rag/build_index.py

# Detect mode and set app flags
if [ "$CODESPACES" = "true" ]; then
  echo "🌐 Detected Codespaces environment. Using Hugging Face mode by default."
  sed -i.bak 's/USE_OLLAMA = True/USE_OLLAMA = False/' app.py
  sed -i.bak 's/USE_OLLAMA = True/USE_OLLAMA = False/' ingest.py
else
  echo ""
  echo "Choose the mode to run TravelBot:"
  echo "1. Local (Ollama + TinyLLaMA)"
  echo "2. Codespaces / Hugging Face (Flan-T5 or TinyLLaMA)"
  read -p "Enter 1 or 2: " mode_choice

  if [ "$mode_choice" == "1" ]; then
    echo "🧠 Setting up for LOCAL mode using Ollama..."
    if ! command -v ollama &> /dev/null; then
        echo "⚠️ Ollama not found. Install it from https://ollama.com"
    else
        ollama pull tinyllama
        sed -i.bak 's/USE_OLLAMA = False/USE_OLLAMA = True/' app.py
        sed -i.bak 's/USE_OLLAMA = False/USE_OLLAMA = True/' ingest.py
    fi
  elif [ "$mode_choice" == "2" ]; then
    echo "🌐 Using Hugging Face mode..."
    sed -i.bak 's/USE_OLLAMA = True/USE_OLLAMA = False/' app.py
    sed -i.bak 's/USE_OLLAMA = True/USE_OLLAMA = False/' ingest.py
  else
    echo "❌ Invalid choice. Please edit app.py manually."
  fi
fi

echo ""
echo "✅ Setup complete."
echo "👉 To start: source .venv/bin/activate && python app.py"
