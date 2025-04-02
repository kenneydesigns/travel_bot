# TravelBot

**AF PCS Travel Assistant powered by RAG + LangChain + Hugging Face LLMs**

TravelBot is a lightweight Retrieval-Augmented Generation (RAG) chatbot that answers questions using uploaded Joint Travel Regulation (JTR) and DAFI (Department of the Air Force Instruction) content. This version is designed to be deployed instantly in GitHub Codespaces.

---

## 🧰 Features

- Uses Hugging Face's `flan-t5-small` or `flan-t5-base` for fast, CPU-compatible inference
- Supports LangChain's `RetrievalQA` pipeline with a local FAISS vectorstore
- Semantic chunk indexing of `.txt` files placed in `rag/jtr_chunks/`
- Persistent prompt guidance from `.txt` files in `context/`
- Setup script builds your environment and prepares the index automatically

---

## 🚀 Quick Start in Codespaces
**⚠️ If setup fails**, you can re-run it manually:
```bash
bash setup.sh
```

1. **Open this repo in GitHub Codespaces**
2. Setup will run automatically from `devcontainer.json`
3. After setup completes, activate your virtual environment:

   ```bash
   source .venv/bin/activate
   ```

4. Start the bot:

   ```bash
   python app.py
   ```

5. Ask questions like:

   - "How many days of parental leave can I take?"
   - "What receipts do I need for my PCS move?"

---

## 🛠 Folder Structure

```bash
├── app.py                  # Main CLI chat app
├── setup.sh                # Environment setup script
├── rag/
│   ├── build_index.py      # Converts text chunks into FAISS vectorstore
│   ├── retrieve_context.py # (optional) Context chunk retriever helper
│   └── jtr_chunks/         # Folder for regulation .txt files
├── context/                # Prompt-level context files (not embedded)
├── vectordb/               # Saved FAISS index (auto-generated)
├── requirements.txt        # Python dependencies
```

---

## 📄 Adding Your Own Content

### 🔹 Regulation Files (JTR/DAFI)
1. Add your `.txt` files to `rag/jtr_chunks/`
2. Run:

```bash
python rag/build_index.py
```

This will rebuild the FAISS vector index.

### 🔹 Prompt Context Files
Add `.txt` files to the `context/` folder (e.g., `bot_intro.txt`, `tone.txt`, `definitions.txt`).  
These are **automatically loaded and prepended** to each question to improve response quality and consistency.

---

## 🔄 Switching Models

The default model is `flan-t5-small`. To improve performance:

```python
model_id = "google/flan-t5-base"
```

Update this line in `app.py` to improve answer quality at the cost of slightly more memory.

---

## ⚙️ Switching to Local Ollama LLM (Optional)

This bot supports both Hugging Face models and local Ollama setups.

- `setup.sh` auto-detects your environment
- For local mode, install [Ollama](https://ollama.com) and run:

```bash
ollama pull tinyllama
```

---

## 📚 Referenced Sources

- JTR PDF (03/01/2025 edition)
- DAFI 36-3003 (7 August 2024)
- Regulation-specific `.txt` files placed in `rag/jtr_chunks/`
- Prompt formatting and tone guidance from `.txt` files in `context/`

---

## ✅ Status

This is a working RAG prototype designed for rapid deployment, expansion, and experimentation.

Coming soon:
- [ ] Chat memory
- [ ] Source citation formatting
- [ ] Web UI (Gradio/FastAPI)
- [ ] Auto-chunker for PDFs

---

Contributions welcome — fork and extend!
