import faiss
import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
import numpy as np

# Paths
data_dir = Path(__file__).resolve().parents[1] / "data"
chunks_file = data_dir / "rag_docs_chunks.txt"
index_file = data_dir / "faiss_index.bin"
metadata_file = data_dir / "metadata.json"

# Load embedding model (CPU-friendly)
print("Loading embedding model...")
model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

# Read chunks
print("Reading chunks...")
chunks = []
with open(chunks_file, "r", encoding="utf-8") as f:
    current_chunk = []
    for line in f:
        line = line.strip()
        if line.startswith("=== CHUNK"):
            if current_chunk:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
        else:
            if line:
                current_chunk.append(line)

    if current_chunk:
        chunks.append(" ".join(current_chunk))

print(f"Total chunks loaded: {len(chunks)}")

# Generate embeddings
print("Generating embeddings...")
embeddings = model.encode(chunks, show_progress_bar=True)
embeddings = np.array(embeddings).astype("float32")

# Create FAISS index
dim = embeddings.shape[1]
index = faiss.IndexFlatL2(dim)
index.add(embeddings)

# Save FAISS index
faiss.write_index(index, str(index_file))
print(f"FAISS index saved to {index_file.name}")

# Save metadata
metadata = [{"chunk_id": i, "text": chunks[i]} for i in range(len(chunks))]
with open(metadata_file, "w", encoding="utf-8") as f:
    json.dump(metadata, f, ensure_ascii=False, indent=2)

print(f"Metadata saved to {metadata_file.name}")
print("Embedding generation completed successfully!")
