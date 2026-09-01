import numpy as np

from app.retrieval.vector_store import (
    VectorStore,
)


def test_faiss_search():

    vectors = np.array(
        [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [0.9, 0.1, 0.0],
        ],
        dtype="float32",
    )

    store = VectorStore(
        dimension=3
    )

    store.add(vectors)

    query = np.array(
        [[1.0, 0.0, 0.0]],
        dtype="float32",
    )

    scores, indices = store.search(
        query,
        top_k=2,
    )

    assert indices.shape == (1, 2)

    assert indices[0][0] == 0

    print("\nScores:", scores)
    print("Indices:", indices)