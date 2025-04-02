import os
import torch

from langchain_community.vectorstores import FAISS
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from langchain_huggingface.llms import HuggingFacePipeline

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

# Load system context
with open("context/bot_intro.txt", "r") as f:
    intro_context = f.read()

# ✅ Final single CLI block
if __name__ == "__main__":
    print("✈️ AF TravelBot is ready. Ask your JTR/DAFI questions.")
    while True:
        query = input("\n> ")
        if query.lower() in ["exit", "quit"]:
            break

        # Inject system prompt with user query
        prompt = f"""{intro_context}

User question: {query}
Answer:"""

        result = qa_chain(prompt)
        
        response = result["result"].strip()
if response.lower() in ["yes", "no"]:
    response += "\n\n(Please verify details in the sources listed below. Travel entitlements may vary based on PCS type and location.)"


        print("\nAnswer:\n", response)
        print("\nSources:")
        for doc in result["source_documents"]:
            print(f"- {doc.metadata['source']}")
