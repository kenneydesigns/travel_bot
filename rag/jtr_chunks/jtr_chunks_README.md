# 📂 /rag/jtr_chunks - Regulation Knowledge Base

This folder contains the **raw .txt files** used to build the FAISS vector store that powers TravelBot's regulation-aware responses.

## 🧠 Purpose

These are not system prompts. These are the searchable **knowledge chunks** from the Joint Travel Regulations (JTR), DAFIs, or supporting guides. They are processed into semantic embeddings and used for **retrieval-augmented generation (RAG)**.

## 📎 How to Use

1. **Add `.txt` files here** — each file should cover a single topic (e.g., `dafi_parental_leave.txt` or `pov_shipping.txt`)
2. **Run the index builder**:

```bash
python rag/build_index.py
```

This will:
- Chunk the documents (500-character blocks with 50-character overlap)
- Embed them
- Save the vector index to `vectordb/travelbot.faiss`

## ✍️ File Naming Tips

Use descriptive, kebab-case file names like:
- `voucher_checklist.txt`
- `tdy_vs_pcs.txt`
- `cola_overview.txt`
- `housing_allowance.txt`

## 🧠 What Makes a Good Chunk File?

- Clear bullet points or paragraph summaries
- Limited to **one topic per file**
- Does **not** repeat other files
- Written in a way that makes sense out of context

## 🛠 Format Example

```txt
=== Cost of Living Allowance (COLA) ===

- Paid to offset high cost of living at certain duty stations
- Applies to OCONUS and select CONUS areas
- Based on location, pay grade, years of service, and number of dependents
- Does not count toward retirement
```

## ⚠️ Important

- Don’t add full JTR or DAFI PDFs here — use `/context` or pre-chunk them
- Always rebuild the index after changes

Happy chunking! 🔍
