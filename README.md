# 🛫 TravelBot: Air Force PCS Chatbot (LLaMA + LangChain + RAG)

Get started with TravelBot using GitHub Codespaces or your local environment. TravelBot helps answer PCS and TDY questions using official sources like the JTR and DAFI36-3003.

---


## 🚀 Setup Guide

### 1. **Create a Codespace**
- Click the green “Code” button on this repo.
- Select “Create codespace on main”.

---

### 2. **Wait for Setup Script**
- git add .devcontainer/devcontainer.json setup.sh
git commit -m "Add devcontainer + executable setup.sh"
git push

---

### 3. **Start TravelBot**
In the terminal, run:

```bash
python app.py
```

Then open the forwarded port at:

```
http://localhost:7860
```

---

### 4. **Ask Your First Question**

Use the web form to ask:
- What receipts do I need to keep for PCS?
- Can I use my GTC for fuel?
- What’s the difference between DTS and eFinance?

---

### 5. **Use Locally (Optional)**

```bash
git clone https://github.com/kenneydesigns/travel_bot.git
cd travel_bot
python3 -m venv .venv
source .venv/bin/activate
bash setup.sh
```

---

### 6. **Use Ollama Locally (Optional)**

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull tinyllama
```

---

### 7. **Expose Public URL (Optional)**

```bash
cloudflared tunnel --url http://localhost:7860
```

---

## 🧾 Project Structure

```
├── app.py
├── rag/
│   ├── build_index.py
│   ├── retrieve_context.py
│   ├── jtr_chunks/
├── models/
├── web/templates/
├── data/
│   ├── JTR.pdf
│   └── dafi36-3003.pdf
├── setup.sh
├── requirements.txt
```

---

## 🧬 Contributing

- Submit new regulation chunks to `rag/jtr_chunks/`
- Suggest UI/UX improvements or integrations
- Pull requests welcome!

---

## 🧺 Credits

- Built by [@kenneydesigns](https://github.com/kenneydesigns)
- LLaMA by Ollama
- RAG with FAISS + LangChain
- UI with Flask

---

Happy building! 🦙
