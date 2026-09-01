from dataclasses import dataclass, field


@dataclass
class ResearchState:

    session_id: int

    research_question: str

    research_questions: list[str] = field(
        default_factory=list
    )

    source_count: int = 0

    chunk_count: int = 0

    finding_count: int = 0

    comparison_count: int = 0

    status: str = "created"

    error: str | None = None