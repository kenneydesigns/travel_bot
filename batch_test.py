import csv
from retrieve_context import qa_chain  # This reuses your LLM + retriever setup

INPUT_FILE = "test_prompts.txt"
OUTPUT_FILE = "results.csv"

with open(INPUT_FILE, "r") as f:
    prompts = [line.strip() for line in f if line.strip()]

with open(OUTPUT_FILE, "w", newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Prompt", "Response", "Sources"])

    for prompt in prompts:
        print(f"🔎 Processing: {prompt}")
        result = qa_chain(prompt)
        sources = "; ".join([doc.metadata['source'] for doc in result['source_documents']])
        writer.writerow([prompt, result["result"], sources])

print(f"\n✅ Finished. Results saved to {OUTPUT_FILE}")
