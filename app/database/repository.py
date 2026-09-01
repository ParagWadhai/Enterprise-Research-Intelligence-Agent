from sqlalchemy.orm import Session
from app.database.models import Source
from app.database.models import Contradiction

from app.database.models import (
    ResearchSession,
    ResearchQuestion,
)
from app.database.models import (
    Document,
    Chunk,
    Finding,
    Evidence,
)

from app.database.models import (
    Conclusion,
)

import json

def create_research_session(
    db: Session,
    question: str
) -> ResearchSession:

    session = ResearchSession(
        question=question,
        status="created"
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return session


def get_research_session(
    db: Session,
    session_id: int
) -> ResearchSession | None:

    return (
        db.query(ResearchSession)
        .filter(
            ResearchSession.id == session_id
        )
        .first()
    )

def create_research_question(
    db,
    session_id: int,
    question: str,
    category: str,
):

    research_question = ResearchQuestion(
        session_id=session_id,
        question=question,
        category=category,
        status="pending",
    )

    db.add(research_question)
    db.commit()
    db.refresh(research_question)

    return research_question

def source_exists(
    db,
    url: str,
) -> bool:

    source = (
        db.query(Source)
        .filter(Source.url == url)
        .first()
    )

    return source is not None


def create_source(
    db,
    session_id: int,
    title: str,
    url: str,
    content: str,
    quality_score: float,
    source_type: str = "web",
):

    source = Source(
        session_id=session_id,
        title=title,
        url=url,
        content=content,
        quality_score=quality_score,
        source_type=source_type,
    )

    db.add(source)
    db.commit()
    db.refresh(source)

    return source

def create_document(
    db,
    source_id: int,
    content: str,
    content_hash: str | None = None,
):

    document = Document(
        source_id=source_id,
        content=content,
        content_hash=content_hash,
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document


def create_chunk(
    db,
    document_id: int,
    chunk_index: int,
    content: str,
):

    chunk = Chunk(
        document_id=document_id,
        chunk_index=chunk_index,
        content=content,
    )

    db.add(chunk)
    db.commit()
    db.refresh(chunk)

    return chunk

def get_document_by_source(
    db,
    source_id: int,
):

    return (
        db.query(Document)
        .filter(
            Document.source_id == source_id
        )
        .first()
    )

def delete_document_chunks(
    db,
    document_id: int,
):

    (
        db.query(Chunk)
        .filter(
            Chunk.document_id == document_id
        )
        .delete(
            synchronize_session=False
        )
    )

    db.commit()

def create_finding(
    db,
    session_id: int,
    finding: str,
    category: str | None,
    classification: str | None,
    confidence: float | None,
):

    finding_obj = Finding(
        session_id=session_id,
        finding=finding,
        category=category,
        classification=classification,
        confidence=confidence,
    )

    db.add(finding_obj)
    db.commit()
    db.refresh(finding_obj)

    return finding_obj

def create_evidence(
    db,
    finding_id: int,
    source_id: int,
    chunk_id: int | None,
    evidence_text: str,
    strength: str | None = None,
):

    evidence = Evidence(
        finding_id=finding_id,
        source_id=source_id,
        chunk_id=chunk_id,
        evidence_text=evidence_text,
        strength=strength,
    )

    db.add(evidence)
    db.commit()
    db.refresh(evidence)

    return evidence

def create_contradiction(
    db,
    finding_a_id: int,
    finding_b_id: int,
    comparison_type: str,
    description: str,
    severity: str | None = None,
):

    contradiction = Contradiction(
        finding_a_id=finding_a_id,
        finding_b_id=finding_b_id,
        comparison_type=comparison_type,
        description=description,
        severity=severity,
    )

    db.add(contradiction)
    db.commit()
    db.refresh(contradiction)

    return contradiction

def get_findings_for_session(
    db,
    session_id: int,
):

    return (
        db.query(Finding)
        .filter(
            Finding.session_id == session_id
        )
        .all()
    )

def create_conclusion(
    db,
    session_id: int,
    executive_summary: str,
    conclusion: str,
    reasoning: str,
    recommendations: list[str],
    risks: list[str],
    confidence: float,
):

    conclusion_obj = Conclusion(
        session_id=session_id,
        executive_summary=executive_summary,
        conclusion=conclusion,
        reasoning=reasoning,
        recommendations=json.dumps(
            recommendations
        ),
        risks=json.dumps(
            risks
        ),
        confidence=confidence,
    )

    db.add(conclusion_obj)
    db.commit()
    db.refresh(conclusion_obj)

    return conclusion_obj