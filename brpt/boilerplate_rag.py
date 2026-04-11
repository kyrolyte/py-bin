import os
import glob
import chromadb
import ollama
from sentence_transformers import SentenceTransformer

# ==============================
# Configuration
# ==============================

EMBED_MODEL = "all-MiniLM-L6-v2"
LLM_MODEL = "qwen3.5"
KNOWLEDGE_DIR = "./knowledge"
COLLECTION_NAME = "code_rag"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
TOP_K = 5


# ==============================
# Embedding Model
# ==============================

print("Loading embedding model...")
embedder = SentenceTransformer(EMBED_MODEL)


# ==============================
# Vector Database
# ==============================

client = chromadb.Client()
collection = client.get_or_create_collection(COLLECTION_NAME)


# ==============================
# Utility: Chunk Text
# ==============================

def chunk_text(text, size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    chunks = []
    start = 0

    while start < len(text):
        end = start + size
        chunk = text[start:end]
        chunks.append(chunk)
        start += size - overlap

    return chunks


# ==============================
# Load Knowledge Files
# ==============================

def load_documents():

    docs = []

    extensions = ["*.py", "*.js", "*.ts", "*.cpp", "*.java", "*.txt", "*.md"]

    for ext in extensions:
        paths = glob.glob(os.path.join(KNOWLEDGE_DIR, ext))

        for path in paths:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()

            chunks = chunk_text(text)

            for chunk in chunks:
                docs.append(chunk)

    return docs


# ==============================
# Index Documents
# ==============================

def index_documents():

    docs = load_documents()

    if len(docs) == 0:
        print("No documents found in knowledge folder.")
        return

    print(f"Indexing {len(docs)} chunks...")

    for i, doc in enumerate(docs):

        emb = embedder.encode(doc).tolist()

        collection.add(
            ids=[f"doc_{i}"],
            embeddings=[emb],
            documents=[doc]
        )

    print("Indexing complete.")


# ==============================
# Retrieve Relevant Context
# ==============================

def retrieve_context(query):

    q_emb = embedder.encode(query).tolist()

    results = collection.query(
        query_embeddings=[q_emb],
        n_results=TOP_K
    )

    docs = results["documents"][0]

    context = "\n\n".join(docs)

    return context


# ==============================
# Build Prompt
# ==============================

def build_prompt(question, context):

    prompt = f"""
You are an expert software engineer.

Use the reference code and documentation below to solve the task.

REFERENCE MATERIAL:
{context}

TASK:
{question}

RULES:
- Return working code
- Use best practices
- Add helpful comments
- If multiple languages are possible, choose the most appropriate
- Output code first, then explanation
"""

    return prompt


# ==============================
# Query LLM
# ==============================

def generate_answer(question):

    context = retrieve_context(question)

    prompt = build_prompt(question, context)

    response = ollama.chat(
        model=LLM_MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response["message"]["content"]


# ==============================
# Interactive CLI
# ==============================

def interactive_chat():

    print("\nLocal RAG Coding Assistant")
    print("Type 'exit' to quit\n")

    while True:

        question = input(">>> ")

        if question.lower() in ["exit", "quit"]:
            break

        answer = generate_answer(question)

        print("\n" + answer + "\n")


# ==============================
# Main
# ==============================

def main():

    print("Checking knowledge base...")

    if collection.count() == 0:
        index_documents()

    interactive_chat()


if __name__ == "__main__":
    main()
