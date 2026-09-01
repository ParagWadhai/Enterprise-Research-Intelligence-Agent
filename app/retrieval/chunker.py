import re


def split_sentences(text: str) -> list[str]:
    """
    Split text into reasonably complete sentences.
    """

    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    if not text:
        return []

    sentences = re.split(
        r"(?<=[.!?])\s+",
        text
    )

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


def chunk_text(
    text: str,
    chunk_size: int = 1200,
    overlap_sentences: int = 2,
) -> list[str]:
    """
    Create chunks using sentence boundaries.

    chunk_size:
        Approximate maximum characters per chunk.

    overlap_sentences:
        Number of sentences carried into the next chunk.
    """

    if not text:
        return []

    sentences = split_sentences(text)

    if not sentences:
        return []

    chunks = []

    current_sentences = []
    current_length = 0

    for sentence in sentences:

        sentence_length = len(sentence)

        # If adding this sentence would exceed the target,
        # finalize the current chunk.
        if (
            current_sentences
            and current_length + sentence_length > chunk_size
        ):

            chunks.append(
                " ".join(current_sentences)
            )

            # Keep the last few sentences as overlap.
            current_sentences = current_sentences[
                -overlap_sentences:
            ]

            current_length = sum(
                len(item)
                for item in current_sentences
            )

        current_sentences.append(sentence)

        current_length += (
            sentence_length + 1
        )

    # Add final chunk
    if current_sentences:

        chunks.append(
            " ".join(current_sentences)
        )

    return chunks