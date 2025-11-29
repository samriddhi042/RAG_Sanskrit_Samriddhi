from pathlib import Path

data_dir = Path(__file__).resolve().parents[1] / "data"

def clean_file(input_name: str, output_name: str):
    in_path = data_dir / input_name
    out_path = data_dir / output_name

    if not in_path.exists():
        print(f"Input file not found: {in_path}")
        return

    print(f"Cleaning {in_path.name} ...")

    text = in_path.read_text(encoding="utf-8")

    # Split into lines, strip spaces, and remove empty lines
    cleaned_lines = []
    for line in text.splitlines():
        line = line.strip()
        if line:  # keep only non-empty lines
            cleaned_lines.append(line)

    cleaned_text = "\n\n".join(cleaned_lines)

    out_path.write_text(cleaned_text, encoding="utf-8")
    print(f"Saved cleaned file as {out_path.name}")

# Clean both files
clean_file("Rag-docs.txt", "Rag-docs_clean.txt")
clean_file("AI-ml intern assignment.txt", "AI-ml intern assignment_clean.txt")

print("All cleaning done.")
