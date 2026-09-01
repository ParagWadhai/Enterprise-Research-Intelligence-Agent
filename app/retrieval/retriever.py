import json

from pathlib import Path

from app.retrieval.embeddings import (
    embedding_service,
)

from app.retrieval.vector_store import (
    VectorStore,
)

from app.database.models import (
    Chunk,
    Document,
    Source,
)


MAPPING_PATH = Path(
    "data/vector_store/chunk_mapping.json"
)


def retrieve_chunks(
    db,
    query: str,
    top_k: int = 5,
):

    vector_store = VectorStore(
        dimension=384
    )

    vector_store.load()

    if vector_store.vectors.shape[0] == 0:
        return []

    query_vector = (
        embedding_service.embed_query(
            query
        )
    )

    scores, indices = (
        vector_store.search(
            query_vector,
            top_k=top_k,
        )
    )

    if not MAPPING_PATH.exists():
        return []

    with open(
        MAPPING_PATH,
        "r",
        encoding="utf-8",
    ) as file:

        mapping = json.load(file)

    results = []

    for score, index in zip(
        scores[0],
        indices[0],
    ):

        if index < 0:
            continue

        chunk_id = mapping.get(
            str(index)
        )

        if chunk_id is None:
            continue

        chunk = (
            db.query(Chunk)
            .filter(
                Chunk.id == int(chunk_id)
            )
            .first()
        )

        if not chunk:
            continue

        document = (
            db.query(Document)
            .filter(
                Document.id == chunk.document_id
            )
            .first()
        )

        if not document:
            continue

        source = (
            db.query(Source)
            .filter(
                Source.id == document.source_id
            )
            .first()
        )

        if not source:
            continue

        results.append(
            {
                "chunk_id": chunk.id,
                "document_id": document.id,
                "source_id": source.id,
                "content": chunk.content,
                "score": float(score),
                "source": {
                    "title": source.title,
                    "url": source.url,
                    "publisher": source.publisher,
                    "quality_score": source.quality_score,
                },
            }
        )

    return results