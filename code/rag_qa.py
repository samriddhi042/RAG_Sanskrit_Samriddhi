import json
from pathlib import Path
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import ollama

# --------------------------
# CONFIG
# --------------------------

MODEL_NAME = "phi3:mini"

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
INDEX_PATH = DATA_DIR / "faiss_index.bin"
META_PATH = DATA_DIR / "metadata.json"

# --------------------------
# LOAD INDEX + METADATA
# --------------------------

print("\nLoading FAISS index...")
index = faiss.read_index(str(INDEX_PATH))

print("Loading metadata...")
with open(META_PATH, "r", encoding="utf-8") as f:
    metadata = json.load(f)

print("Loading embedding model...")
embedder = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

# --------------------------
# RAG FUNCTION
# --------------------------

def answer_query(query):
    print("\nEmbedding query...")
    query_embedding = embedder.encode([query])

    print("Searching index...")
    distances, indices = index.search(np.array(query_embedding).astype("float32"), 3)

    retrieved_chunks = []
    for idx in indices[0]:
        chunk_item = metadata[idx]

        # Extract text correctly (metadata may be dict or string)
        if isinstance(chunk_item, dict):
            retrieved_chunks.append(chunk_item.get("text", ""))
        else:
            retrieved_chunks.append(chunk_item)

    # Combine all retrieved text chunks
    context = "\n\n".join(retrieved_chunks)

    final_prompt = f"""
Use the following context to answer the question.
If the answer is not clearly available in the context, say "I don't know".

Context:
{context}

Question: {query}

Answer:
"""

    print("\nQuerying Ollama local model...")
    result = ollama.generate(
        model=MODEL_NAME,
        prompt=final_prompt
    )

    return result["response"]

# --------------------------
# MAIN LOOP
# --------------------------

if __name__ == "__main__":
    print("\n✨ Sanskrit RAG System using Ollama (phi3:mini) ✨")
    print("Type 'exit' to quit.\n")

    while True:
        query = input("Ask a question: ")
        if query.lower() in ["exit", "quit"]:
            break

        response = answer_query(query)
        print("\n--- ANSWER ---")
        print(response)
        print("---------------\n")
