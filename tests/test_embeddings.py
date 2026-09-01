from app.retrieval.embeddings import (
    embedding_service,
)


def test_embeddings():

    texts = [
        "AI is transforming retail operations.",
        "Machine learning is used for demand forecasting.",
    ]

    vectors = embedding_service.embed(
        texts
    )

    assert vectors.shape[0] == 2

    assert vectors.shape[1] > 0

    print(
        "\nEmbedding shape:",
        vectors.shape
    )