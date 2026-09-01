from pathlib import Path

import numpy as np


VECTOR_STORE_PATH = Path(
    "data/vector_store/vectors.npy"
)


class VectorStore:

    def __init__(self, dimension: int):

        self.dimension = dimension

        self.vectors = np.empty(
            (0, dimension),
            dtype="float32"
        )

    def add(self, vectors):

        vectors = np.asarray(
            vectors,
            dtype="float32"
        )

        if vectors.ndim == 1:
            vectors = vectors.reshape(1, -1)

        if vectors.shape[1] != self.dimension:
            raise ValueError(
                f"Expected dimension {self.dimension}, "
                f"got {vectors.shape[1]}"
            )

        self.vectors = np.vstack(
            [self.vectors, vectors]
        )

    def search(
        self,
        query_vector,
        top_k: int = 5,
    ):

        query_vector = np.asarray(
            query_vector,
            dtype="float32"
        )

        if query_vector.ndim == 1:
            query_vector = query_vector.reshape(1, -1)

        # Embeddings are already normalized,
        # so dot product = cosine similarity.
        scores = np.dot(
            query_vector,
            self.vectors.T
        )

        top_k = min(
            top_k,
            self.vectors.shape[0]
        )

        indices = np.argsort(
            -scores[0]
        )[:top_k]

        top_scores = scores[
            0,
            indices
        ]

        return (
            top_scores.reshape(1, -1),
            indices.reshape(1, -1)
        )

    def save(self):

        VECTOR_STORE_PATH.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        np.save(
            VECTOR_STORE_PATH,
            self.vectors,
        )

    def load(self):

        if not VECTOR_STORE_PATH.exists():
            return

        self.vectors = np.load(
            VECTOR_STORE_PATH
        )