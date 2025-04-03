# TravelBot

**TravelBot** is a regulation-grounded assistant designed to help users navigate Air Force travel rules (JTR, DAFI 36-3003, AFMAN 65-114) using Retrieval-Augmented Generation (RAG). It supports Hugging Face and Ollama LLMs and works seamlessly in GitHub Codespaces or on a local machine.

---

## ✨ Features

- 🔍 Vector-based regulation search using LangChain + FAISS
- 🤖 Friendly or Raw chatbot mode (via `retrieve_context.py`)
- 📄 Direct chunk retrieval mode (via `chunkbot.py`)
- 🧠 Prompt-aware assistant using `app.py` + context files
- 📂 Auto-updated knowledge base from uploaded regulation PDFs
- 🔁 Supports Hugging Face models *or* local Ollama LLMs
- ⚡ Fast, lean, token-efficient, and customizable

---

## 🚀 Get Started in GitHub Codespaces or Locally

1. Open the repo in GitHub Codespaces or clone locally  
2. Run the setup script:

```bash
bash setup.sh
```

3. Then activate your environment and run the chatbot:

```bash
source .venv/bin/activate
python retrieve_context.py --mode friendly
```

💡 If you’re testing from a fresh environment, this flow ensures everything is installed and indexed before your first question.

---

## 🧠 How to Use TravelBot

### ✅ Option 1: `retrieve_context.py` – Flexible CLI Chatbot

Supports two modes:
- `--mode friendly`: Uses an LLM to add a natural intro
- `--mode raw`: Outputs regulation text only (no LLM generation)

```bash
python retrieve_context.py --mode friendly
python retrieve_context.py --mode raw
```

---

### ✅ Option 2: `chunkbot.py` – Search-Only Tool

- No LLM used
- Retrieves top regulation chunks directly
- Great for debugging or validation

```bash
python chunkbot.py
```

---

### ✅ Option 3: `app.py` – Prompt-Controlled Chatbot

- Loads system prompt + tone guidance from `context/`
- Uses LangChain's RetrievalQA chain
- Token-limited, clean, predictable

```bash
python app.py
```

---

## 🔄 Updating the Regulation Knowledge Base

When JTR or DAFI updates:
1. Drop PDFs into:
```
rag/source_docs/
```

2. Run:
```bash
python update_knowledge_base.py
```

This extracts text, chunks it with `RecursiveCharacterTextSplitter`, and rebuilds the FAISS vector index.

---

## 🧰 Folder Structure

```
├── retrieve_context.py         # CLI chatbot with friendly/raw toggle
├── chunkbot.py                 # Direct semantic chunk retriever
├── app.py                      # Context-aware LLM QA chatbot
├── update_knowledge_base.py    # Auto-chunker + vector index builder
├── setup.sh                    # Bootstraps environment + installs dependencies
├── context/                    # Optional .txt files for system prompt and tone
├── rag/
│   ├── jtr_chunks/             # .txt chunks from JTR/DAFI/AFMAN regs
│   ├── source_docs/            # Drop your PDFs here
├── vectordb/                   # FAISS index files (auto-generated)
├── requirements.txt            # Dependency list
```

---

## 🤖 Switching Between LLMs

### Use a Hugging Face model:
Inside `retrieve_context.py` or `app.py`, update:
```python
model_id = "google/flan-t5-small"  # or flan-t5-base
```

### Use local Ollama:
1. Install [Ollama](https://ollama.com)
2. Pull a model:
```bash
ollama pull tinyllama
```
3. Modify `setup.sh` or `retrieve_context.py` to load the Ollama LLM instead of Hugging Face

---

## 📘 Source Materials

TravelBot can index and respond based on:
- JTR (March 2025)
- DAFI 36-3003 (August 2024)
- AFMAN 65-114 (current)
- Any `.pdf` you drop into `rag/source_docs/`

---

## 📅 Roadmap

- [ ] Add Gradio or FastAPI web UI
- [ ] Add chat memory / history
- [ ] Add evaluator scoring / confidence indicator
- [ ] Add embedded link-back to reg source section

---

## 🙌 Contributing

Fork it, remix it, deploy it at your unit.  
TravelBot is built to help Airmen and DoD staff get answers without combing through thousands of pages.

