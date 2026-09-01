import json
import re

from typing import Literal

from pydantic import BaseModel

from app.ai.llm import generate_response


# ---------------------------------------------------------
# Pydantic schemas
# ---------------------------------------------------------


class ComparisonResult(BaseModel):

    finding_a_id: int

    finding_b_id: int

    comparison_type: Literal[
        "support",
        "contradiction",
        "partial_agreement",
    ]

    description: str

    severity: Literal[
        "low",
        "medium",
        "high",
    ]

    model_config = {
        "extra": "forbid"
    }


class ComparisonResponse(BaseModel):

    comparisons: list[ComparisonResult]

    model_config = {
        "extra": "forbid"
    }
# ---------------------------------------------------------
# System prompt
# ---------------------------------------------------------

SYSTEM_PROMPT = """
You are an enterprise research evidence comparison analyst.

Your task is to compare research findings.

You must ONLY use the findings provided.

Your primary goal is to identify meaningful relationships,
especially contradictions.

Possible relationships:

- support
- contradiction
- partial_agreement

Definitions:

support:
Two findings generally reinforce each other.

contradiction:
Two findings make materially incompatible claims
about the same subject, context, and condition.

partial_agreement:
The findings agree on some aspects but differ on others.

Important rules:

1. Different wording does NOT automatically mean contradiction.
2. Do not invent facts.
3. Do not invent evidence.
4. Use only the supplied finding IDs.
5. Only compare meaningfully related findings.
6. Do not compare unrelated findings.
7. Keep descriptions very short.
8. Do not repeat the original findings.
9. Do not include evidence text.
10. Return ONLY valid JSON.
11. Do not use markdown.
12. Do not add commentary before or after JSON.

Severity must be one of:

- low
- medium
- high
"""


# ---------------------------------------------------------
# JSON cleaning
# ---------------------------------------------------------

def _clean_json(response: str) -> str:

    response = response.strip()

    # Remove ```json
    response = re.sub(
        r"^```json\s*",
        "",
        response,
        flags=re.IGNORECASE,
    )

    # Remove ```
    response = re.sub(
        r"\s*```$",
        "",
        response,
    )

    return response.strip()


# ---------------------------------------------------------
# Build finding input
# ---------------------------------------------------------

def _build_findings_text(
    findings: list[dict],
) -> str:

    findings_text = []

    for item in findings:

        evidence_ids = [
            {
                "chunk_id": evidence["chunk_id"],
                "source_id": evidence["source_id"],
            }
            for evidence in item.get(
                "evidence",
                []
            )
        ]

        findings_text.append(
            f"""
FINDING_ID: {item['finding_id']}

FINDING:
{item['finding']}

CATEGORY:
{item['category']}

CLASSIFICATION:
{item['classification']}

CONFIDENCE:
{item['confidence']}

EVIDENCE_REFERENCES:
{json.dumps(evidence_ids)}
"""
        )

    return "\n".join(findings_text)


# ---------------------------------------------------------
# Validate comparison values
# ---------------------------------------------------------

def _validate_comparisons(
    validated: ComparisonResponse,
):

    allowed_types = {
        "support",
        "contradiction",
        "partial_agreement",
    }

    allowed_severity = {
        "low",
        "medium",
        "high",
    }

    for comparison in validated.comparisons:

        if (
            comparison.comparison_type
            not in allowed_types
        ):

            raise ValueError(
                "Invalid comparison type: "
                f"{comparison.comparison_type}"
            )

        if (
            comparison.severity
            not in allowed_severity
        ):

            raise ValueError(
                "Invalid severity: "
                f"{comparison.severity}"
            )


# ---------------------------------------------------------
# Main comparison function
# ---------------------------------------------------------

def compare_findings(
    findings: list[dict],
) -> dict:

    # -----------------------------------------------------
    # Not enough findings to compare
    # -----------------------------------------------------

    if len(findings) < 2:

        return {
            "comparisons": []
        }

    findings_text = _build_findings_text(
        findings
    )

    # -----------------------------------------------------
    # First LLM request
    # -----------------------------------------------------

    user_prompt = f"""
Compare the following research findings.

{findings_text}

Your primary goal is to detect contradictions.

Rules:

1. Compare only findings discussing the same or closely
   related topic.
2. Do NOT report unrelated findings.
3. Do NOT compare every possible pair.
4. Return at most 10 comparisons.
5. Prioritize contradictions.
6. Then report strong supporting relationships.
7. Keep each description under 20 words.
8. Do not repeat the findings.
9. Do not include evidence text.
10. Use only the supplied finding IDs.
11. Return ONLY valid JSON.

Allowed comparison_type values:

- support
- contradiction
- partial_agreement

Allowed severity values:

- low
- medium
- high

Return exactly:

{{
    "comparisons": [
        {{
            "finding_a_id": 15,
            "finding_b_id": 16,
            "comparison_type": "support",
            "description": "Both identify AI as improving manufacturing efficiency.",
            "severity": "low"
        }}
    ]
}}

If there are no meaningful relationships, return:

{{
    "comparisons": []
}}
"""

    # response = generate_response(
    #     system_prompt=SYSTEM_PROMPT,
    #     user_prompt=user_prompt,
    # )
    response = generate_response(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=user_prompt,
        response_schema=ComparisonResponse,
    )

    cleaned = _clean_json(
        response
    )

    # -----------------------------------------------------
    # Try first response
    # -----------------------------------------------------

    try:

        result = json.loads(
            cleaned
        )

    except json.JSONDecodeError as exc:

        print(
            "\n⚠️ Comparison JSON invalid."
        )

        print(
            f"Line: {exc.lineno}"
        )

        print(
            f"Column: {exc.colno}"
        )

        print(
            f"Error: {exc.msg}"
        )

        print(
            "🔄 Retrying with smaller prompt..."
        )

        # -------------------------------------------------
        # Retry prompt
        # -------------------------------------------------

        retry_prompt = f"""
Return ONLY valid JSON.

Analyze these research findings:

{findings_text}

Find ONLY:

1. Contradictions
2. Strong support relationships

Maximum 5 comparisons.

Keep each description under 15 words.

Allowed comparison_type:

- support
- contradiction
- partial_agreement

Allowed severity:

- low
- medium
- high

Use only the supplied finding IDs.

Return exactly:

{{
    "comparisons": [
        {{
            "finding_a_id": 15,
            "finding_b_id": 16,
            "comparison_type": "support",
            "description": "Both identify operational AI benefits.",
            "severity": "low"
        }}
    ]
}}

If there are no meaningful relationships:

{{
    "comparisons": []
}}

Do not use markdown.
Do not include commentary.
"""

        retry_response = generate_response(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=retry_prompt,
        )

        retry_cleaned = _clean_json(
            retry_response
        )

        try:

            result = json.loads(
                retry_cleaned
            )

        except json.JSONDecodeError as retry_exc:

            print(
                "\n========== COMPARISON RETRY FAILED =========="
            )

            print(
                retry_cleaned
            )

            print(
                "\nJSON ERROR:"
            )

            print(
                f"Line: {retry_exc.lineno}"
            )

            print(
                f"Column: {retry_exc.colno}"
            )

            print(
                f"Message: {retry_exc.msg}"
            )

            print(
                "==============================================\n"
            )

            raise ValueError(
                "Groq returned invalid JSON "
                "for evidence comparison "
                "even after retry."
            ) from retry_exc

    # -----------------------------------------------------
    # Pydantic validation
    # -----------------------------------------------------

    validated = (
        ComparisonResponse.model_validate(
            result
        )
    )

    # -----------------------------------------------------
    # Business validation
    # -----------------------------------------------------

    _validate_comparisons(
        validated
    )

    return validated.model_dump()