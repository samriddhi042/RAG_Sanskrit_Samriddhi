# Sanskrit RAG System (Internship Assignment)

This project is a Retrieval-Augmented Generation (RAG) system that answers questions from Sanskrit stories using a local CPU-based language model.

## 1. What this project does

- Reads Sanskrit text from `Rag-docs.docx`
- Cleans and splits it into chunks
- Creates embeddings and a FAISS index
- Uses a local model (via Ollama: `phi3:mini`) to answer questions based on the retrieved chunks

## 2. Folder structure (important folders)

- `code/` – all Python scripts
- `data/` – input docs, cleaned text, chunks, FAISS index, metadata
- `report/` – final report (to be added)
- `venv/` – virtual environment (not needed on GitHub)

## 3. How to set up (steps)

1. Create and activate virtual environment:

   ```bash
   python -m venv venv
   venv\Scripts\activate

## 4. Install required packages:

pip install sentence-transformers faiss-cpu ollama python-docx numpy

## 5. Install Ollama (if not installed):

Download from https://ollama.com/download and install.

## 6. Pull the local model:

ollama pull phi3:mini

## 7. How to rebuild the pipeline (optional)

Run these scripts in order:

python code/docx_to_txt.py       # .docx -> .txt
python code/clean_texts.py       # clean text
python code/chunk_sanskrit.py    # create chunks
python code/create_embeddings.py # embeddings + FAISS index

## 8. How to test retrieval only (optional)
python code/query_index.py

## 9. How to run the final RAG question-answer system
python code/rag_qa.py

Then type a question, for example:

मूर्खभृत्यस्य कथायाः सारांशः लिख।

What is the moral of the bell story?

The system will:

Embed the question

Search the FAISS index

Retrieve relevant Sanskrit text

Ask the local model (phi3:mini) to generate an answer

