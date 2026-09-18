import chromadb

# 1) Create a client (in-memory database)
client = chromadb.Client()

# 2) Create a collection with an embedding function
collection = client.create_collection(
    name="my_notes",
    embedding_function=None,  # None = we pass embeddings manually
)

# 3) Sample documents
documents = [
    "The cat sits on the mat",
    "A kitten is sleeping on a rug",
    "I love programming in Python",
    "The stock market went up today",
]
ids = ["doc1", "doc2", "doc3", "doc4"]

# 4) Generate embeddings with sentence-transformers
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(documents).tolist()

# 5) Add documents to the collection
collection.add(
    documents=documents,
    embeddings=embeddings,
    ids=ids,
)

print(f"Stored {collection.count()} documents\n")

# 6) Query with a semantic question
query = "A small cat is resting"
query_embedding = model.encode(query).tolist()

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3,
)

print(f"Query: {query!r}\n")
for i, (doc, distance) in enumerate(zip(results["documents"][0], results["distances"][0]), 1):
    print(f"  {i}. {doc}  (distance: {distance:.4f})")
