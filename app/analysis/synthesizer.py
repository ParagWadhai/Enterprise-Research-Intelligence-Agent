import json
import re

from app.ai.llm import generate_response


SYSTEM_PROMPT = """
You are an enterprise research synthesis analyst.

Your job is to create a final research report using ONLY
the findings, evidence, source information, and contradiction
information provided to you.

Do NOT introduce facts that are not supported by the input.

The report must:

1. Summarize the research for a business executive.
2. Identify the most important findings.
3. Explain the reasoning behind the conclusion.
4. Identify important risks.
5. Provide practical recommendations.
6. Consider contradictory evidence.
7. Avoid presenting uncertain information as fact.
8. Clearly distinguish evidence from inference.

Important:

- Do not invent sources.
- Do not invent statistics.
- Do not invent evidence.
- Do not claim certainty when evidence conflicts.
- Recommendations should follow from the findings.
- Confidence must reflect evidence quality and contradictions.

Return ONLY valid JSON.
"""


def _clean_json(
    response: str,
) -> str:

    response = response.strip()

    response = re.sub(
        r"^```json\s*",
        "",
        response,
        flags=re.IGNORECASE,
    )

    response = re.sub(
        r"\s*```$",
        "",
        response,
    )

    return response.strip()


def synthesize_research(
    research_question: str,
    findings: list[dict],
    comparisons: list[dict],
) -> dict:

    findings_text = []

    for finding in findings:

        evidence_text = "\n".join(
            [
                (
                    f"Chunk {e['chunk_id']} "
                    f"(Source {e['source_id']}): "
                    f"{e['evidence_text']}"
                )
                for e in finding.get(
                    "evidence",
                    []
                )
            ]
        )

        findings_text.append(
            f"""
FINDING_ID: {finding['finding_id']}

FINDING:
{finding['finding']}

CATEGORY:
{finding['category']}

CLASSIFICATION:
{finding['classification']}

CONFIDENCE:
{finding['confidence']}

EVIDENCE:
{evidence_text}
"""
        )

    comparisons_text = []

    for comparison in comparisons:

        comparisons_text.append(
            f"""
Finding {comparison['finding_a_id']}
vs
Finding {comparison['finding_b_id']}

TYPE:
{comparison['comparison_type']}

DESCRIPTION:
{comparison['description']}

SEVERITY:
{comparison['severity']}
"""
        )

    user_prompt = f"""
RESEARCH QUESTION:

{research_question}


RESEARCH FINDINGS:

{"".join(findings_text)}


EVIDENCE COMPARISONS:

{"".join(comparisons_text)}


Create the final enterprise research report.

Return exactly:

{{
    "executive_summary": "...",

    "conclusion": "...",

    "reasoning": "...",

    "recommendations": [
        "..."
    ],

    "risks": [
        "..."
    ],

    "confidence": 0.0
}}
"""

    response = generate_response(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=user_prompt,
    )

    cleaned = _clean_json(
        response
    )

    try:

        return json.loads(
            cleaned
        )

    except json.JSONDecodeError as exc:

        raise ValueError(
            "Groq returned invalid JSON "
            "for research synthesis."
        ) from exc