import os
import argparse

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from langchain_community.llms import HuggingFacePipeline

# Load lightweight LLM
model_id = "google/flan-t5-base"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForSeq2SeqLM.from_pretrained(model_id)
pipe = pipeline("text2text-generation", model=model, tokenizer=tokenizer, max_new_tokens=100)
llm = HuggingFacePipeline(pipeline=pipe)

# Load vector store
db = FAISS.load_local(
    "vectordb",
    HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"),
    index_name="travelbot",
    allow_dangerous_deserialization=True
)
retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 2})

# Source version tags
source_version_map = {
    "jtr_mar2025_chunk0.txt": "JTR (March 2025)",
    "afman65-114_chunk0.txt": "AFMAN 65-114",
    "dafi36-3003_chunk0.txt": "DAFI 36-3003"
}

def format_sources(retrieved):
    labels = set()
    for doc in retrieved:
        fname = doc.metadata["source"]
        label = source_version_map.get(fname, fname.split("_chunk")[0])
        labels.add(label)
    return "\n".join(f"- {label}" for label in sorted(labels))

def hybrid_response(query):
    # Step 1: LLM-friendly preface
    pre_prompt = f"The user asked: '{query}'. Write a helpful, conversational introduction before showing regulation content."
    preface = str(llm(pre_prompt)).strip()

    # Step 2: Retrieve raw regulation chunks
    retrieved = retriever.get_relevant_documents(query)
    raw_chunks = "\n\n".join(doc.page_content for doc in retrieved)

    # Step 3: Fallback if nothing useful found
    if not retrieved or len(raw_chunks) < 200:
        return f"{preface}\n\nI couldn’t find a specific regulation that clearly answers this. You may want to consult your FSO or check JTR guidance for your PDS.\n\n---\nSources:\n{format_sources(retrieved)}"

    # Step 4: Output both
    return f"{preface}\n\n---\n{raw_chunks}\n\n---\nSources:\n{format_sources(retrieved)}"

# CLI loop
parser = argparse.ArgumentParser(description="AF TravelBot CLI")
parser.add_argument("--mode", choices=["friendly", "raw"], default="friendly", help="Choose response style.")
args = parser.parse_args()

retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 3})

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

def run_cli():
    print("✈️ AF TravelBot is ready. Ask your JTR/DAFI questions.")
    while True:
        query = input("\n> ")
        if query.lower() in ["exit", "quit"]:
            break
        result = qa_chain(query)
        print("\nAnswer:\n", result["result"])
        print("\nSources:")
        for doc in result["source_documents"]:
            print(f"- {doc.metadata['source']}")

if __name__ == "__main__":
    run_cli()

# Ensure qa_chain is available for import
__all__ = ["qa_chain"]

