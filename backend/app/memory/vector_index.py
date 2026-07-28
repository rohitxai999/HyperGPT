import faiss
import numpy as np


class VectorIndex:

    def __init__(self, dimension=384):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.memory_ids = []

    def add(self, memory_id: int, embedding: list):
        vector = np.array([embedding], dtype="float32")
        self.index.add(vector)
        self.memory_ids.append(memory_id)

    def search(self, embedding: list, k: int = 5):
        if self.index.ntotal == 0:
            return []

        vector = np.array([embedding], dtype="float32")

        distances, indices = self.index.search(vector, k)

        results = []

        for idx, distance in zip(indices[0], distances[0]):
            if idx == -1:
                continue

            results.append({
                "memory_id": self.memory_ids[idx],
                "distance": float(distance)
            })

        return results

    def total_vectors(self):
        return self.index.ntotal