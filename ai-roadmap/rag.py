import chromadb
from dotenv import load_dotenv
from openai import OpenAI
from sentence_transformers import SentenceTransformer

load_dotenv()  # Load OPENAI_API_KEY from .env

# ---- 1. Embedding model ----
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# ---- 2. Vector store ----
client = chromadb.Client()
collection = client.get_or_create_collection(name="ai_knowledge")

# ---- 3. Knowledge base (chunks of knowledge) ----
documents = [
    "Tokenization splits text into tokens (integer IDs) that a model can read.",
    "Embeddings convert text into dense vectors that capture semantic meaning.",
    "Cosine similarity measures the angle between two vectors to find similar texts.",
    "A vector database stores embeddings and enables fast similarity search.",
    "RAG (Retrieval-Augmented Generation) retrieves relevant documents and feeds them to an LLM.",
    "RAG reduces hallucinations by grounding the model's answer in retrieved context.",
    "RAG has two stages: retrieval (find relevant docs) and generation (write the answer).",
    "MCP (Model Context Protocol) lets AI agents use external tools and servers.",
    "Function calling lets an LLM request a specific tool/function to be executed.",
    "Semantic search finds documents by meaning, not just exact keyword matching.",
]

ids = [f"doc{i}" for i in range(len(documents))]
embeddings = embed_model.encode(documents).tolist()
collection.add(documents=documents, embeddings=embeddings, ids=ids)

print(f"Indexed {collection.count()} chunks\n")

# ---- 4. Query ----
query = "What is RAG and how does it work?"

results = collection.query(
    query_texts=[query],
    n_results=3,
    include=["documents", "distances"],
)
retrieved = results["documents"][0]
distances = results["distances"][0]

print("Retrieved context:")
for i, (doc, dist) in enumerate(zip(retrieved, distances), 1):
    print(f"  [{i}] (distance={dist:.4f}) {doc}")
print()

# ---- 5. Generate the answer with an LLM ----
llm = OpenAI()  # Reads OPENAI_API_KEY from environment

context = "\n".join(f"- {doc}" for doc in retrieved)

prompt = f"""You are a helpful AI tutor.
Answer the question using ONLY the context below.
Write a clear explanation in 2-3 sentences.

Context:
{context}

Question: {query}

Answer:"""

response = llm.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    temperature=0,
)

print("=" * 50)
print("Final answer:")
print(response.choices[0].message.content)
