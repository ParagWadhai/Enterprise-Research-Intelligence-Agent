from app.retrieval.retriever import (
    retrieve_chunks,
)

from app.analysis.finding_analyzer import (
    analyze_evidence,
)

from app.database.repository import (
    create_finding,
    create_evidence,
)

from app.database.models import (
    Finding,
    Evidence,
)

def analyze_research_question(
    db,
    session_id: int,
    query: str,
    top_k: int = 8,
):

    retrieved_evidence = retrieve_chunks(
        db=db,
        query=query,
        top_k=top_k,
    )

    if not retrieved_evidence:

        return {
            "session_id": session_id,
            "query": query,
            "findings": [],
        }

    analysis = analyze_evidence(
        query=query,
        retrieved_evidence=retrieved_evidence,
    )

    saved_findings = []

    for item in analysis.get(
        "findings",
        []
    ):

        finding = create_finding(
            db=db,
            session_id=session_id,
            finding=item["finding"],
            category=item.get(
                "category"
            ),
            classification=item.get(
                "classification"
            ),
            confidence=item.get(
                "confidence"
            ),
        )

        saved_evidence = []

        for evidence_ref in item.get(
            "evidence",
            []
        ):

            chunk_id = evidence_ref.get(
                "chunk_id"
            )

            source_id = evidence_ref.get(
                "source_id"
            )

            matching_chunk = next(
                (
                    evidence
                    for evidence
                    in retrieved_evidence
                    if evidence["chunk_id"]
                    == chunk_id
                    and evidence["source_id"]
                    == source_id
                ),
                None,
            )

            if not matching_chunk:
                continue

            evidence = create_evidence(
                db=db,
                finding_id=finding.id,
                source_id=source_id,
                chunk_id=chunk_id,
                evidence_text=matching_chunk[
                    "content"
                ],
                strength=(
                    "strong"
                    if matching_chunk[
                        "score"
                    ] >= 0.75
                    else "moderate"
                ),
            )

            saved_evidence.append(
                {
                    "chunk_id": chunk_id,
                    "source_id": source_id,
                    "score": matching_chunk[
                        "score"
                    ],
                }
            )

        saved_findings.append(
            {
                "finding_id": finding.id,
                "finding": finding.finding,
                "category": finding.category,
                "classification": (
                    finding.classification
                ),
                "confidence": finding.confidence,
                "evidence": saved_evidence,
            }
        )

    return {
        "session_id": session_id,
        "query": query,
        "findings": saved_findings,
    }

def get_finding_with_evidence(
    db,
    finding_id: int,
):

    finding = (
        db.query(Finding)
        .filter(
            Finding.id == finding_id
        )
        .first()
    )

    if not finding:
        return []

    evidence_rows = (
        db.query(Evidence)
        .filter(
            Evidence.finding_id
            == finding_id
        )
        .all()
    )

    return [
        {
            "evidence_id": evidence.id,
            "chunk_id": evidence.chunk_id,
            "source_id": evidence.source_id,
            "evidence_text": (
                evidence.evidence_text
            ),
            "strength": evidence.strength,
        }
        for evidence in evidence_rows
    ]