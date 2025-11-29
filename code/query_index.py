import faiss
import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
import numpy as np

# Paths
data_dir = Path(__file__).resolve().parents[1] / "data"
index_file = data_dir / "faiss_index.bin"
metadata_file = data_dir / "metadata.json"

# Load FAISS index
print("Loading FAISS index...")
index = faiss.read_index(str(index_file))

# Load metadata
print("Loading metadata...")
with open(metadata_file, "r", encoding="utf-8") as f:
    metadata = json.load(f)

# Load embedding model (same as before)
print("Loading embedding model...")
model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

def search(query: str, top_k: int = 3):
    # Convert query to embedding
    query_emb = model.encode([query])
    query_emb = np.array(query_emb).astype("float32")

    # Search in FAISS index
    distances, indices = index.search(query_emb, top_k)

    print(f"\nTop {top_k} results for query: {query}")
    for rank, (idx, dist) in enumerate(zip(indices[0], distances[0]), start=1):
        chunk_info = metadata[idx]
        print(f"\n--- Result {rank} (chunk_id={chunk_info['chunk_id']}, distance={dist:.4f}) ---")
        print(chunk_info["text"])

def main():
    print("Interactive search ready!")
    print("Type 'exit' to quit.\n")

    while True:
        query = input("Enter your question (Sanskrit or English): ").strip()
        if query.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break
        if not query:
            continue

        search(query, top_k=3)

if __name__ == "__main__":
    main()
