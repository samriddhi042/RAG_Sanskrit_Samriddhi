from pathlib import Path

data_dir = Path(__file__).resolve().parents[1] / "data"

INPUT_FILE = "Rag-docs_clean.txt"
OUTPUT_FILE = "rag_docs_chunks.txt"

# You can tweak these if needed
CHUNK_SIZE_WORDS = 250
OVERLAP_WORDS = 50

def load_text():
    path = data_dir / INPUT_FILE
    if not path.exists():
        raise FileNotFoundError(f"Cannot find {path}")
    text = path.read_text(encoding="utf-8")
    return text

def make_chunks(text: str):
    # We will split based on whitespace (spaces/newlines)
    words = text.split()
    chunks = []

    i = 0
    n = len(words)

    while i < n:
        # Take CHUNK_SIZE_WORDS words
        chunk_words = words[i : i + CHUNK_SIZE_WORDS]
        if not chunk_words:
            break
        chunk = " ".join(chunk_words)
        chunks.append(chunk)

        # Move index forward with overlap
        i += CHUNK_SIZE_WORDS - OVERLAP_WORDS

    return chunks

def save_chunks(chunks):
    out_path = data_dir / OUTPUT_FILE

    with out_path.open("w", encoding="utf-8") as f:
        for idx, chunk in enumerate(chunks, start=1):
            f.write(f"=== CHUNK {idx} ===\n")
            f.write(chunk)
            f.write("\n\n")

    print(f"Saved {len(chunks)} chunks to {out_path.name}")

def main():
    print("Loading cleaned Sanskrit text...")
    text = load_text()
    print("Creating chunks...")
    chunks = make_chunks(text)
    print(f"Total chunks: {len(chunks)}")
    save_chunks(chunks)

if __name__ == "__main__":
    main()
