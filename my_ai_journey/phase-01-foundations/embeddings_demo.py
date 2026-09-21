import numpy as np


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


# Toy 2D embeddings (just to visualize the idea)
cat = np.array([1.0, 0.8])
dog = np.array([0.9, 0.7])
car = np.array([-0.8, 0.6])
banana = np.array([-0.9, 0.5])

print("Similarity (cat, dog), 4 (cat, dog):", round(cosine_similarity(cat, dog), 4))
print("Similarity (cat, car):", round(cosine_similarity(cat, car), 4))
print("Similarity (car, banana):", round(cosine_similarity(car, banana), 4))
