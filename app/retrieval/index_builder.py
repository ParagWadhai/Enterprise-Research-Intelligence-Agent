import json

from pathlib import Path

from app.retrieval.embeddings import (
    embedding_service,
)

from app.retrieval.vector_store import (
    VectorStore,
)


MAPPING_PATH = Path(
    "data/vector_store/chunk_mapping.json"
)


def build_index_for_chunks(
    db,
    chunks,
):

    if not chunks:
        return None

    texts = [
        chunk.content
        for chunk in chunks
    ]

    vectors = embedding_service.embed(
        texts
    )

    vector_store = VectorStore(
        dimension=vectors.shape[1]
    )

    vector_store.add(
        vectors
    )

    vector_store.save()

    mapping = {
        str(index): chunk.id
        for index, chunk in enumerate(chunks)
    }

    MAPPING_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        MAPPING_PATH,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            mapping,
            file,
            indent=2,
        )

    return vector_store