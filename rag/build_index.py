from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
import os

# Build documents from all .txt files
docs = []
for filename in os.listdir("rag/jtr_chunks"):
    if filename.endswith(".txt"):
        with open(os.path.join("rag/jtr_chunks", filename), "r") as f:
            text = f.read()
            docs.append(Document(page_content=text, metadata={"source": filename}))

# Split and embed
splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Save vector DB
db = FAISS.from_documents(chunks, embeddings)
db.save_local("vectordb", index_name="travelbot")
