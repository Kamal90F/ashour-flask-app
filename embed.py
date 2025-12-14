import os
import json
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from openai import OpenAI
import faiss
import numpy as np

# Load API Key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -----------------------------------------
# 1. Load PDFs and extract text
# -----------------------------------------
def load_pdfs(folder="data"):
    all_text = ""
    for file in os.listdir(folder):
        if file.endswith(".pdf"):
            reader = PdfReader(os.path.join(folder, file))
            for page in reader.pages:
                all_text += page.extract_text() + "\n"
    return all_text


# -----------------------------------------
# 2. Split text into chunks
# -----------------------------------------
def split_text(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )
    return splitter.split_text(text)


# -----------------------------------------
# 3. Create embeddings using OpenAI
# -----------------------------------------
def embed_chunks(chunks):
    vectors = []
    for chunk in chunks:
        response = client.embeddings.create(
            model="text-embedding-3-small",   # Best + cheap embedding model
            input=chunk
        )
        vectors.append(response.data[0].embedding)
    return np.array(vectors).astype("float32")


# -----------------------------------------
# 4. Save embeddings to FAISS + chunks to JSON
# -----------------------------------------
def save_faiss(vectors, chunks):
    index = faiss.IndexFlatL2(vectors.shape[1])
    index.add(vectors)
    faiss.write_index(index, "embeddings/faiss_index.bin")

    with open("embeddings/chunks.json", "w") as f:
        json.dump(chunks, f)


# -----------------------------------------
# RUN ALL STEPS
# -----------------------------------------
def build_embedding():
    print("Loading PDFs...")
    text = load_pdfs()

    print("Splitting into chunks...")
    chunks = split_text(text)

    print(f"Total chunks: {len(chunks)}")

    print("Embedding chunks...")
    vectors = embed_chunks(chunks)

    print("Saving FAISS index...")
    save_faiss(vectors, chunks)

    print("Embedding complete! You can now run query.py")


if __name__ == "__main__":
    build_embedding()
