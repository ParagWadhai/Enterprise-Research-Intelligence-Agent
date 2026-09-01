from app.retrieval.chunker import chunk_text


def test_chunk_text():

    text = """
    AI is transforming retail operations.
    Retailers use AI for demand forecasting.
    AI can improve inventory management.
    AI enables dynamic pricing.
    AI can personalize customer experiences.
    """

    chunks = chunk_text(
        text,
        chunk_size=100,
        overlap_sentences=1,
    )

    assert len(chunks) > 1

    for chunk in chunks:

        assert chunk.strip()

        # Chunks should not begin or end
        # with obvious partial words.
        assert not chunk.startswith("e ")
        assert not chunk.endswith("e")

    print("\nChunks:")

    for index, chunk in enumerate(chunks):

        print(
            f"\nChunk {index}:"
        )

        print(chunk)