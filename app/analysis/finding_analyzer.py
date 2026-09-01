import json

from app.ai.llm import generate_response
from app.schemas.finding import (
    FindingAnalysisResponse,
)


SYSTEM_PROMPT = """
You are an enterprise research analyst.

You analyze ONLY the evidence provided to you.

Do not use unsupported outside knowledge.

Your job is to:

1. Extract the most important findings.
2. Classify each finding.
3. Estimate confidence.
4. Link every finding to supporting evidence.

Possible categories include:
- Technology
- Operations
- Benefits
- Risks
- Adoption
- Cost
- Customer Experience
- Workforce
- Strategy

Possible classifications include:
- Adoption
- Emerging
- Benefit
- Risk
- Trend
- Challenge
- Evidence

IMPORTANT OUTPUT LIMITS:

- Return AT MOST 5 findings.
- Prefer 3 to 5 high-value findings.
- Never return more than 5 findings.
- Do not create duplicate findings.
- Do not summarize every piece of evidence.
- Select only the most important insights.
- Keep each finding concise.
- Keep each finding under 30 words.

Evidence rules:

- Do not invent facts.
- Do not create sources.
- Every finding must reference one or more provided chunk IDs.
- Confidence must be between 0 and 1.
- If evidence is weak, lower the confidence.
- Prefer multiple independent sources when available.
- Only reference chunk IDs that appear in the provided evidence.
- Only reference source IDs that appear in the provided evidence.
- chunk_id and source_id MUST be integers, not strings.

JSON rules:

- Return ONLY the requested JSON object.
- Do not return markdown.
- Do not add commentary.
- Do not rename fields.
- Do not add fields.
- Every finding MUST contain:
  finding
  category
  classification
  confidence
  evidence
- Every evidence item MUST contain:
  chunk_id
  source_id
"""


def analyze_evidence(
    query: str,
    retrieved_evidence: list[dict],
) -> dict:

    if not retrieved_evidence:

        return {
            "findings": []
        }

    # =====================================================
    # Prepare evidence
    # =====================================================

    evidence_text = []

    for item in retrieved_evidence:

        evidence_text.append(
            f"""
SOURCE_ID: {item['source_id']}
CHUNK_ID: {item['chunk_id']}
SOURCE_TITLE: {item['source']['title']}
SOURCE_URL: {item['source']['url']}
SOURCE_QUALITY: {item['source']['quality_score']}
SIMILARITY_SCORE: {item['score']}

EVIDENCE:
{item['content']}
"""
        )

    # =====================================================
    # User prompt
    # =====================================================

    user_prompt = f"""
Research Question:

{query}

Retrieved Evidence:

{"".join(evidence_text)}

Analyze the evidence and extract the most important findings.

IMPORTANT:

- Return between 3 and 5 findings when sufficient evidence exists.
- NEVER return more than 5 findings.
- Select only the strongest and most relevant findings.
- Do not repeat similar findings.
- Do not try to cover every sentence in the evidence.
- Keep each finding under 30 words.
- Every finding must contain all required fields.
- Use only the supplied chunk IDs and source IDs.
- chunk_id and source_id MUST be integers, not strings.
- Do not put line breaks inside JSON field names.
- Use exactly the field name "finding".

Return the structured research findings.
"""

    # =====================================================
    # Groq structured output
    # =====================================================

    response = generate_response(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=user_prompt,
        response_schema=FindingAnalysisResponse,
    )

    # =====================================================
    # Parse JSON
    # =====================================================

    try:

        result = json.loads(response)

    except json.JSONDecodeError as exc:

        print(
            "\n========== GROQ INVALID JSON =========="
        )

        print(response)

        print(
            "\nJSON ERROR:"
        )

        print(
            f"Line: {exc.lineno}"
        )

        print(
            f"Column: {exc.colno}"
        )

        print(
            f"Message: {exc.msg}"
        )

        print(
            "=======================================\n"
        )

        raise ValueError(
            "Groq returned invalid JSON "
            f"at line {exc.lineno}, "
            f"column {exc.colno}: "
            f"{exc.msg}"
        ) from exc

    # =====================================================
    # Validate against Pydantic schema
    # =====================================================

    validated = (
        FindingAnalysisResponse.model_validate(
            result
        )
    )

    # =====================================================
    # Final safety check
    # =====================================================

    if len(validated.findings) > 5:

        raise ValueError(
            "Finding analysis returned more than "
            "5 findings."
        )

    return validated.model_dump()