import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


sentences = [
    "The cat sits on the mat",
    "A kitten is sleeping on a rug",
    "I love programming in Python",
    "The stock market went up today",
]

embeddings = model.encode(sentences)
print("Embedding shape:", embeddings.shape)  # (4, 384)

query = "A small cat is resting"
query_embedding = model.encode(query)

print(f"\nQuery: {query!r}\n")
for sentence, emb in zip(sentences, embeddings):
    score = cosine_similarity(query_embedding, emb)
    print(f"  {score:.3f}  |  {sentence}")
