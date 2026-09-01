from pydantic import BaseModel, Field


class EvidenceReference(BaseModel):

    chunk_id: int

    source_id: int

    model_config = {
        "extra": "forbid"
    }


class FindingResult(BaseModel):

    finding: str

    category: str

    classification: str

    confidence: float = Field(
        ge=0.0,
        le=1.0
    )

    evidence: list[
        EvidenceReference
    ]

    model_config = {
        "extra": "forbid"
    }


class FindingAnalysisResponse(BaseModel):

    findings: list[
        FindingResult
    ]

    model_config = {
        "extra": "forbid"
    }