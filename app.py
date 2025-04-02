USE_OLLAMA = False  # Set to True for local Ollama, False for Hugging Face

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import HuggingFacePipeline

if USE_OLLAMA:
    from langchain.llms import Ollama
    from langchain.embeddings.ollama import OllamaEmbeddings

    print("💻 Running in LOCAL mode using Ollama + TinyLLaMA")
    embeddings = OllamaEmbeddings(model="tinyllama")
    llm = Ollama(model="tinyllama")

else:
    from langchain.llms import HuggingFacePipeline
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

    print("🌐 Running in CODESPACES mode using Hugging Face model")
    model_id = "google/flan-t5-base"

    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_id)

    pipe = pipeline("text2text-generation", model=model, tokenizer=tokenizer, max_length=512)
    llm = HuggingFacePipeline(pipeline=pipe)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Load the vector DB
db = FAISS.load_local(
    "vectordb",
    embeddings=embeddings,
    index_name="travelbot",
    allow_dangerous_deserialization=True
)

# Create chain
qa = RetrievalQA.from_chain_type(llm=llm, retriever=db.as_retriever())

# Chat loop
print("TravelBot is ready. Ask a question or type 'exit'.")
while True:
    query = input("You: ")
    if query.lower() in ["exit", "quit"]:
        break
    answer = qa.run(query)
    print("Bot:", answer)
with open("chat_log.txt", "a") as log:
    log.write(f"\n---\nQ: {question}\nA: {answer}\n")
USE_OLLAMA = False  # Set to True for local Ollama, False for Hugging Face

from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings

if USE_OLLAMA:
    from langchain.llms import Ollama
    from langchain.embeddings.ollama import OllamaEmbeddings

    print("💻 Running in LOCAL mode using Ollama + TinyLLaMA")
    embeddings = OllamaEmbeddings(model="tinyllama")
    llm = Ollama(model="tinyllama")

else:
    from langchain.llms import HuggingFacePipeline
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

    print("🌐 Running in CODESPACES mode using Hugging Face model")
    model_id = "google/flan-t5-base"

    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_id)

    pipe = pipeline("text2text-generation", model=model, tokenizer=tokenizer, max_length=512)
    llm = HuggingFacePipeline(pipeline=pipe)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Load the vector DB
db = FAISS.load_local("vectordb", embeddings=embeddings, index_name="travelbot")

# Create QA chain
qa = RetrievalQA.from_chain_type(llm=llm, retriever=db.as_retriever())

# Chat loop
print("🧳 TravelBot is ready. Ask a question or type 'exit'.")
while True:
    query = input("You: ")
    if query.lower() in ["exit", "quit"]:
        print("👋 TravelBot session ended.")
        break
    answer = qa.run(query)
    print("Bot:", answer)

    with open("chat_log.txt", "a") as log:
        log.write(f"\n---\nQ: {query}\nA: {answer}\n")
