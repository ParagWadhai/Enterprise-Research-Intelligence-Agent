from pydantic import BaseModel, Field


class ConclusionResponse(BaseModel):

    session_id: int

    executive_summary: str

    conclusion: str

    reasoning: str

    recommendations: list[str]

    risks: list[str]

    confidence: float = Field(
        ge=0.0,
        le=1.0
    )