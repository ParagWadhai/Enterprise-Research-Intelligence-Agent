import hashlib

from app.retrieval.chunker import chunk_text

from app.database.repository import (
    create_document,
    create_chunk,
    get_document_by_source,
    delete_document_chunks,
)


def calculate_content_hash(
    content: str,
) -> str:

    return hashlib.sha256(
        content.encode("utf-8")
    ).hexdigest()


def process_source(
    db,
    source,
):

    if not source.content:
        return []

    content_hash = calculate_content_hash(
        source.content
    )

    existing_document = (
        get_document_by_source(
            db=db,
            source_id=source.id,
        )
    )

    if existing_document:

        # Remove old chunks because
        # our chunking strategy may have changed.
        delete_document_chunks(
            db=db,
            document_id=existing_document.id,
        )

        document = existing_document

        document.content = source.content
        document.content_hash = content_hash

        db.commit()

    else:

        document = create_document(
            db=db,
            source_id=source.id,
            content=source.content,
            content_hash=content_hash,
        )

    chunks = chunk_text(
        source.content
    )

    created_chunks = []

    for index, chunk_content in enumerate(chunks):

        chunk = create_chunk(
            db=db,
            document_id=document.id,
            chunk_index=index,
            content=chunk_content,
        )

        created_chunks.append(chunk)

    return created_chunks