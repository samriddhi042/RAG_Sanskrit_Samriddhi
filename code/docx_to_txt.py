from docx import Document
from pathlib import Path

# Get the /data folder relative to this file
data_dir = Path(__file__).resolve().parents[1] / "data"

for docx_path in data_dir.glob("*.docx"):
    print(f"Reading {docx_path.name} ...")
    doc = Document(docx_path)
    full_text = []

    # Read all paragraphs
    for para in doc.paragraphs:
        text = para.text.strip()
        if text:
            full_text.append(text)

    # Write to .txt with same name
    txt_path = docx_path.with_suffix(".txt")
    txt_path.write_text("\n\n".join(full_text), encoding="utf-8")
    print(f"Converted {docx_path.name} -> {txt_path.name}")

print("Done converting all .docx files.")
