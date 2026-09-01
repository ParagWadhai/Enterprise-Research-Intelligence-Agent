# from datetime import datetime
from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Float,
    DateTime,
    ForeignKey,
)

from sqlalchemy.orm import relationship

from app.database.database import Base


class ResearchSession(Base):
    __tablename__ = "research_sessions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    question = Column(
        Text,
        nullable=False
    )

    status = Column(
        String(50),
        default="created",
        nullable=False
    )

    progress = Column(
        Integer,
        default=0,
        nullable=False
    )

    current_stage = Column(
        String(100),
        nullable=True
    )

    error_message = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    completed_at = Column(
        DateTime,
        nullable=True
    )

    research_questions = relationship(
        "ResearchQuestion",
        back_populates="session",
        cascade="all, delete-orphan"
    )

    sources = relationship(
        "Source",
        back_populates="session",
        cascade="all, delete-orphan"
    )

    findings = relationship(
        "Finding",
        back_populates="session",
        cascade="all, delete-orphan"
    )

    conclusions = relationship(
        "Conclusion",
        back_populates="session",
        cascade="all, delete-orphan"
    )


class ResearchQuestion(Base):
    __tablename__ = "research_questions"

    id = Column(Integer, primary_key=True, index=True)

    session_id = Column(
        Integer,
        ForeignKey("research_sessions.id"),
        nullable=False
    )

    question = Column(Text, nullable=False)

    category = Column(
        String(100),
        nullable=True
    )

    status = Column(
        String(50),
        default="pending"
    )

    session = relationship(
        "ResearchSession",
        back_populates="research_questions"
    )


class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)

    session_id = Column(
        Integer,
        ForeignKey("research_sessions.id"),
        nullable=False
    )

    title = Column(Text, nullable=False)

    url = Column(Text, nullable=True)

    publisher = Column(
        String(255),
        nullable=True
    )

    source_type = Column(
        String(100),
        nullable=True
    )

    published_date = Column(
        String(100),
        nullable=True
    )

    retrieved_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    content = Column(
        Text,
        nullable=True
    )

    content_hash = Column(
        String(64),
        nullable=True,
        index=True
    )

    quality_score = Column(
        Float,
        nullable=True
    )

    session = relationship(
        "ResearchSession",
        back_populates="sources"
    )

    documents = relationship(
        "Document",
        back_populates="source",
        cascade="all, delete-orphan"
    )

    evidence = relationship(
        "Evidence",
        back_populates="source"
    )


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    source_id = Column(
        Integer,
        ForeignKey("sources.id"),
        nullable=False
    )

    content = Column(
        Text,
        nullable=False
    )

    content_hash = Column(
        String(64),
        nullable=True,
        index=True
    )

    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    source = relationship(
        "Source",
        back_populates="documents"
    )

    chunks = relationship(
        "Chunk",
        back_populates="document",
        cascade="all, delete-orphan"
    )


class Chunk(Base):
    __tablename__ = "chunks"

    id = Column(Integer, primary_key=True, index=True)

    document_id = Column(
        Integer,
        ForeignKey("documents.id"),
        nullable=False
    )

    chunk_index = Column(
        Integer,
        nullable=False
    )

    content = Column(
        Text,
        nullable=False
    )

    document = relationship(
        "Document",
        back_populates="chunks"
    )


class Finding(Base):
    __tablename__ = "findings"

    id = Column(Integer, primary_key=True, index=True)

    session_id = Column(
        Integer,
        ForeignKey("research_sessions.id"),
        nullable=False
    )

    finding = Column(
        Text,
        nullable=False
    )

    category = Column(
        String(100),
        nullable=True
    )

    classification = Column(
        String(100),
        nullable=True
    )

    confidence = Column(
        Float,
        nullable=True
    )

    session = relationship(
        "ResearchSession",
        back_populates="findings"
    )

    evidence = relationship(
        "Evidence",
        back_populates="finding",
        cascade="all, delete-orphan"
    )


class Evidence(Base):
    __tablename__ = "evidence"

    id = Column(Integer, primary_key=True, index=True)

    finding_id = Column(
        Integer,
        ForeignKey("findings.id"),
        nullable=False
    )

    source_id = Column(
        Integer,
        ForeignKey("sources.id"),
        nullable=False
    )

    chunk_id = Column(
        Integer,
        ForeignKey("chunks.id"),
        nullable=True
    )

    evidence_text = Column(
        Text,
        nullable=False
    )

    strength = Column(
        String(50),
        nullable=True
    )

    finding = relationship(
        "Finding",
        back_populates="evidence"
    )

    source = relationship(
        "Source",
        back_populates="evidence"
    )


class Contradiction(Base):
    __tablename__ = "contradictions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    finding_a_id = Column(
        Integer,
        ForeignKey("findings.id"),
        nullable=False
    )

    finding_b_id = Column(
        Integer,
        ForeignKey("findings.id"),
        nullable=False
    )

    comparison_type = Column(
        String(50),
        nullable=False,
        default="contradiction"
    )

    description = Column(
        Text,
        nullable=False
    )

    severity = Column(
        String(50),
        nullable=True
    )

class Conclusion(Base):
    __tablename__ = "conclusions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    session_id = Column(
        Integer,
        ForeignKey("research_sessions.id"),
        nullable=False
    )

    executive_summary = Column(
        Text,
        nullable=False
    )

    conclusion = Column(
        Text,
        nullable=False
    )

    reasoning = Column(
        Text,
        nullable=True
    )

    recommendations = Column(
        Text,
        nullable=True
    )

    risks = Column(
        Text,
        nullable=True
    )

    confidence = Column(
        Float,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    session = relationship(
        "ResearchSession",
        back_populates="conclusions"
    )