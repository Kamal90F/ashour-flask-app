import os
import json
import faiss
import numpy as np
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ------------------------------
# Load FAISS + chunks
# ------------------------------
index = faiss.read_index("embeddings/faiss_index.bin")

with open("embeddings/chunks.json", "r") as f:
    chunks = json.load(f)


# ------------------------------
# Convert question into embedding
# ------------------------------
def get_question_embedding(question):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=question
    )
    return np.array(response.data[0].embedding).astype("float32")


# ------------------------------
# Search FAISS for similar chunks
# ------------------------------
def search_chunks(question, k=3):
    q_vector = get_question_embedding(question)
    q_vector = np.expand_dims(q_vector, axis=0)

    distances, indices = index.search(q_vector, k)

    results = [chunks[i] for i in indices[0]]
    return results


# ------------------------------
# Ask GPT-4o-mini using RAG
# ------------------------------
def ask_tutor(question):
    context = "\n\n".join(search_chunks(question))

    prompt = f"""
You are an AI tutor. Use the following curriculum context to answer the student's question.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER (clear, friendly, step-by-step):
"""

    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


# ------------------------------
# TEST
# ------------------------------
if __name__ == "__main__":
    while True:
        def get_ai_response(q)
        #q = input("\nAsk a question: ")
        return ask_tutor(q)
        #print("\nAnswer:\n", ask_tutor(q))
