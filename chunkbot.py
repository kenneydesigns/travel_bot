import os
import torch

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

model_id = "google/flan-t5-base"
print("📚 Loading ChunkBot with model:", model_id)

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForSeq2SeqLM.from_pretrained(model_id)

pipe = pipeline(
    "text2text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=256,
    do_sample=True,
    temperature=0.7,
    repetition_penalty=1.2,
    top_k=50,
    top_p=0.95
)

from langchain_community.llms import HuggingFacePipeline
llm = HuggingFacePipeline(pipeline=pipe)

retriever = FAISS.load_local(
    "vectordb",
    HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"),
    index_name="travelbot",
    allow_dangerous_deserialization=True
).as_retriever(search_type="similarity", search_kwargs={"k": 3})

print("✅ ChunkBot is ready. Ask your PCS/TDY travel questions.")

while True:
    query = input("\n> ")
    if query.lower() in ["exit", "quit"]:
        break

    print("\n🔍 Retrieving relevant chunk content...")
    docs = retriever.get_relevant_documents(query)

    # Show retrieved text from chunks
    for i, doc in enumerate(docs, 1):
        print(f"\n📄 Source {i}: {doc.metadata['source']}")
        print(doc.page_content.strip())

    summarize = input("\n📝 Summarize the retrieved content with AI? (y/n): ").strip().lower()
    if summarize == "y":
        combined = "\n\n".join([doc.page_content for doc in docs])
        summary_prompt = (
            "Summarize this travel guidance:\n\n"
            + combined
            + "\n\nSummary:"
        )
        summary = llm(summary_prompt)
        print("\n💡 Summary:\n", summary)
