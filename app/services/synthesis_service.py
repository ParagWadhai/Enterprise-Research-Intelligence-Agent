import json

from app.database.repository import (
    get_findings_for_session,
    create_conclusion,
)

from app.database.models import (
    Contradiction,
)

from app.analysis.synthesizer import (
    synthesize_research,
)


def generate_research_conclusion(
    db,
    session_id: int,
):

    findings = (
        get_findings_for_session(
            db=db,
            session_id=session_id,
        )
    )

    if not findings:

        return {
            "session_id": session_id,
            "error": "No findings available."
        }

    # -----------------------------------------
    # Prepare compact findings
    # -----------------------------------------
    #
    # IMPORTANT:
    # Do not send full evidence/chunk content
    # to the synthesis LLM.
    #
    # Evidence was already used during the
    # analysis stage.
    #
    # This keeps the synthesis prompt small.
    # -----------------------------------------

    finding_payloads = []

    for finding in findings:

        finding_payloads.append(
            {
                "finding_id": finding.id,
                "finding": finding.finding,
                "category": finding.category,
                "classification": (
                    finding.classification
                ),
                "confidence": finding.confidence,
            }
        )

    # -----------------------------------------
    # Load comparisons
    # -----------------------------------------

    finding_ids = [
        finding.id
        for finding in findings
    ]

    comparisons = (
        db.query(Contradiction)
        .filter(
            Contradiction.finding_a_id.in_(
                finding_ids
            )
        )
        .all()
    )

    comparison_payloads = [
        {
            "finding_a_id": item.finding_a_id,
            "finding_b_id": item.finding_b_id,
            "comparison_type": (
                item.comparison_type
            ),
            "description": item.description,
            "severity": item.severity,
        }
        for item in comparisons
    ]

    # -----------------------------------------
    # Get original research question
    # -----------------------------------------

    session = findings[0].session

    research_question = session.question

    # -----------------------------------------
    # Groq synthesis
    # -----------------------------------------

    result = synthesize_research(
        research_question=research_question,
        findings=finding_payloads,
        comparisons=comparison_payloads,
    )

    # -----------------------------------------
    # Save conclusion
    # -----------------------------------------

    conclusion = create_conclusion(
        db=db,
        session_id=session_id,
        executive_summary=(
            result["executive_summary"]
        ),
        conclusion=result["conclusion"],
        reasoning=result["reasoning"],
        recommendations=(
            result.get(
                "recommendations",
                []
            )
        ),
        risks=(
            result.get(
                "risks",
                []
            )
        ),
        confidence=result.get(
            "confidence",
            0.0
        ),
    )

    # -----------------------------------------
    # Return response
    # -----------------------------------------

    return {
        "session_id": session_id,

        "executive_summary": (
            conclusion.executive_summary
        ),

        "conclusion": (
            conclusion.conclusion
        ),

        "reasoning": (
            conclusion.reasoning
        ),

        "recommendations": json.loads(
            conclusion.recommendations
            or "[]"
        ),

        "risks": json.loads(
            conclusion.risks
            or "[]"
        ),

        "confidence": (
            conclusion.confidence
        ),
    }