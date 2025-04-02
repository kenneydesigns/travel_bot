import os
query = os.environ.get("QUESTION") or input("\n🔎 Ask a travel question: ")
source_version_map = {
    "dafi36-3003_aug2024.pdf_chunk0.txt": "DAFI 36-3003 (August 2024)",
    "jtr_mar2025.pdf_chunk0.txt": "JTR (March 2025)",
    # Add more mappings as needed
}

def format_response(answer: str, sources: list) -> str:
    preface = "Here's what I found based on official guidance:\n"
    outro = "\nLet me know if you'd like help navigating the next step."

    source_labels = set()
    for doc in sources:
        fname = doc.metadata["source"]
        label = source_version_map.get(fname, fname.split("_chunk")[0])
        source_labels.add(label)

    source_str = "\n\nSource(s):\n" + "\n".join(f"- {label}" for label in sorted(source_labels))
    return f"{preface}{answer}{outro}{source_str}"
if __name__ == "__main__":
    print("✈️ AF TravelBot is ready. Ask your JTR/DAFI questions.")
    while True:
        query = input("\n> ")
        if query.lower() in ["exit", "quit"]:
            break
        result = qa_chain(query)
        print("\n" + format_response(result["result"], result["source_documents"]))
