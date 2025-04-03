import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import fitz  # PyMuPDF

SOURCE_DIR = "rag/source_docs"
CHUNK_DIR = "rag/jtr_chunks"
INDEX_DIR = "vectordb"
INDEX_NAME = "travelbot"

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    return "\n".join(page.get_text().strip() for page in doc)

def split_and_save_chunks(text, base_filename):
    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=30)
    chunks = splitter.create_documents([text])
    saved_count = 0
    for i, chunk in enumerate(chunks):
        if len(chunk.page_content.strip()) > 100:  # Filter out nearly empty chunks
            chunk.metadata = {
                "source": f"{base_filename}_chunk{i}.txt",
                "chunk_index": i,
                "origin": base_filename
            }
            with open(os.path.join(CHUNK_DIR, f"{base_filename}_chunk{i}.txt"), "w") as f:
                f.write(chunk.page_content)
            saved_count += 1
    print(f"✅ Saved {saved_count} valid chunks for {base_filename}")

def rebuild_vector_index():
    documents = []
    for fname in os.listdir(CHUNK_DIR):
        if fname.endswith(".txt"):
            with open(os.path.join(CHUNK_DIR, fname)) as f:
                documents.append(Document(page_content=f.read(), metadata={"source": fname}))
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = FAISS.from_documents(documents, embeddings)
    db.save_local(INDEX_DIR, index_name=INDEX_NAME)
    print("✅ Vector DB updated and saved.")

def run():
    os.makedirs(CHUNK_DIR, exist_ok=True)
    os.makedirs(SOURCE_DIR, exist_ok=True)  # <-- Add this line
    print("🧹 Clearing old chunks...")
    for file in os.listdir(CHUNK_DIR):
        os.remove(os.path.join(CHUNK_DIR, file))

    for file in os.listdir(SOURCE_DIR):
        if file.endswith(".pdf"):
            print(f"📄 Chunking {file}...")
            full_text = extract_text_from_pdf(os.path.join(SOURCE_DIR, file))
            base = os.path.splitext(file)[0]
            split_and_save_chunks(full_text, base)

    rebuild_vector_index()

if __name__ == "__main__":
    run()
