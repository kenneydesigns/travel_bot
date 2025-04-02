import os
import torch

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from langchain_community.llms import HuggingFacePipeline

model_id = "google/flan-t5-small"

print("🪶 Loading lightweight model: FLAN-T5 Small...")

tokenizer = AutoTokenizer.from_pretrained(model_id)

model = AutoModelForSeq2SeqLM.from_pretrained(
    model_id,
    device_map="auto"
)

pipe = pipeline(
    "text2text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=512
)

llm = HuggingFacePipeline(pipeline=pipe)



db = FAISS.load_local(
    "vectordb",
    HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"),
    index_name="travelbot",
    allow_dangerous_deserialization=True
)

retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 3})

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)


# Simple CLI loop
if __name__ == "__main__":
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
