# TravelBot

AF PCS Travel Assistant powered by Retrieval-Augmented Generation (RAG), Hugging Face models, and LangChain.

---

## 🧠 Run Modes

You can use TravelBot through multiple entry points depending on your needs:

### 1. `retrieve_context.py` – The Main Chatbot CLI

Supports two modes:
- **Friendly mode** (default): uses an LLM to generate a helpful intro, then shows retrieved regulation chunks.
- **Raw mode**: shows retrieved chunks only (no LLM).

Run it like this:
```bash
python retrieve_context.py --mode friendly
python retrieve_context.py --mode raw
```

---

### 2. `chunkbot.py` – Direct Chunk Search

- Retrieves the top 3 chunks using vector similarity.
- No LLM, just raw regulation text.
- Great for debugging or validating the source content.

Run:
```bash
python chunkbot.py
```

---

### 3. `app.py` – Alt Chatbot with Intro Context

- Loads a system prompt from a file.
- Uses LangChain's `RetrievalQA` for simpler setups.
- Automatically trims inputs to stay under token limits.

Run:
```bash
python app.py
```

---

## 🔄 Updating the Knowledge Base

1. Place new PDFs in:
```
rag/source_docs/
```

2. Rebuild the chunks and vector index:
```bash
python update_knowledge_base.py
```

---

## 🧰 Setup

From the root of the repo:
```bash
bash setup.sh
```

This will:
- Create `.venv`
- Install dependencies
- Support Hugging Face and Ollama inference options

---

Let me know if you want this copied into your actual `README.md` file or merged with the existing contents.
