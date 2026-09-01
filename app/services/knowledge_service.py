from app.database.models import Source

from app.retrieval.document_processor import (
    process_source,
)

from app.retrieval.index_builder import (
    build_index_for_chunks,
)


def build_knowledge_base(
    db,
    session_id: int,
):

    sources = (
        db.query(Source)
        .filter(
            Source.session_id == session_id
        )
        .all()
    )

    all_chunks = []

    for source in sources:

        chunks = process_source(
            db=db,
            source=source,
        )

        all_chunks.extend(
            chunks
        )

    if not all_chunks:

        return {
            "session_id": session_id,
            "sources_processed": 0,
            "chunks_created": 0,
        }

    build_index_for_chunks(
        db=db,
        chunks=all_chunks,
    )

    return {
        "session_id": session_id,
        "sources_processed": len(sources),
        "chunks_created": len(all_chunks),
    }