import os
import argparse

from langchain.chains import RetrievalQA
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
    # Step 1: Dynamic pre-prompt based on query style
    if any(phrase in query.lower() for phrase in ["difference between", " vs ", "compare", "how is", "which is better"]):
        pre_prompt = (
            f"The user asked: '{query}'. Answer in 2–3 sentences comparing the terms. "
            "Use regulation-based terminology if possible."
        )
    else:
        pre_prompt = (
            f"The user asked: '{query}'. Please explain in a helpful and detailed way using regulation terms if possible."
        )

    # Step 2: Generate the LLM preface with context hint
    context_hint = (
    "You are an Air Force travel assistant who explains military travel rules clearly. "
    "Avoid repeating boilerplate answers. If uncertain, explain that the user should consult an FSO or relevant regulation. "
    "Prioritize clarity, accuracy, and concise structure. Use regulation terms like JTR and DAFI where applicable."
)

    full_prompt = context_hint + "\n\n" + pre_prompt
    preface = str(llm(full_prompt)).strip()

    # Step 3: Retrieve raw regulation chunks
    retrieved = retriever.get_relevant_documents(query)
    raw_chunks = "\n\n".join(doc.page_content for doc in retrieved)

    # Step 4: Fallback if nothing useful found
    if not retrieved or len(raw_chunks) < 200:
        return f"{preface}\n\nI couldn’t find a specific regulation that clearly answers this. You may want to consult your FSO or check JTR guidance for your PDS.\n\n---\nSources:\n{format_sources(retrieved)}"

    # Step 5: Combine preface with retrieved content
    final_response = f"{preface}\n\n---\n{raw_chunks}\n\n---\nSources:\n{format_sources(retrieved)}"

    # Step 6: Handle short responses
    if len(raw_chunks.split()) < 10:
        final_response = "Here's what I found, but please check with your FSO or review the regulation for full details.\n\n" + final_response

    return final_response



# CLI loop
retriever = db.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 5, "lambda_mult": 0.8}
)

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
    query = input("Ask a travel question: ")
    result = qa_chain.run(query)
    print("\nAnswer:\n", result)


# ✅ Only parse args and launch CLI if directly run from terminal
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="AF TravelBot CLI")
    parser.add_argument("--mode", choices=["friendly", "raw"], default="friendly", help="Choose response style.")
    args = parser.parse_args()

    run_cli()


def run_cli():
    print("✈️ AF TravelBot is ready. Ask your JTR/DAFI questions.")
    while True:
        query = input("\n> ")
        if query.lower() in ["exit", "quit"]:
            break
        result = hybrid_response(query)
        print("\nAnswer:\n", result)

if __name__ == "__main__":
    run_cli()

# Ensure qa_chain is available for import
__all__ = ["qa_chain"]

