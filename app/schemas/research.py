from datetime import datetime

from pydantic import BaseModel, Field


class ResearchRequest(BaseModel):

    question: str = Field(
        ...,
        min_length=10,
        max_length=2000,
    )


class ResearchQuestionResponse(BaseModel):
    id: int
    question: str
    category: str | None = None
    status: str | None = None
    progress: int = 0

    current_stage: str | None = None

    error_message: str | None = None


class ResearchResponse(BaseModel):
    session_id: int
    question: str
    status: str
    created_at: datetime

    research_questions: list[
        ResearchQuestionResponse
    ] = []