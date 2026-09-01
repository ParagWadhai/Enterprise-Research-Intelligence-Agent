from app.database.repository import (
    get_findings_for_session,
    create_contradiction,
)

from app.services.analysis_service import (
    get_finding_with_evidence,
)

from app.analysis.evidence_comparator import (
    compare_findings,
)

from app.analysis.confidence import (
    adjust_confidence,
)


def compare_session_findings(
    db,
    session_id: int,
):

    findings = (
        get_findings_for_session(
            db=db,
            session_id=session_id,
        )
    )

    if len(findings) < 2:

        return {
            "session_id": session_id,
            "comparisons": [],
        }

    finding_payloads = []

    for finding in findings:

        evidence = (
            get_finding_with_evidence(
                db=db,
                finding_id=finding.id,
            )
        )

        finding_payloads.append(
            {
                "finding_id": finding.id,
                "finding": finding.finding,
                "category": finding.category,
                "classification": (
                    finding.classification
                ),
                "confidence": finding.confidence,
                "evidence": evidence,
            }
        )

    # Ask Groq to compare the findings
    comparison_result = (
        compare_findings(
            finding_payloads
        )
    )

    saved_comparisons = []

    # Save meaningful comparisons
    for item in comparison_result.get(
        "comparisons",
        []
    ):

        comparison_type = item.get(
            "comparison_type",
            "unrelated"
        )

        # Ignore unrelated findings
        if comparison_type == "unrelated":
            continue

        contradiction = (
            create_contradiction(
                db=db,
                finding_a_id=item[
                    "finding_a_id"
                ],
                finding_b_id=item[
                    "finding_b_id"
                ],
                comparison_type=(
                    comparison_type
                ),
                description=item[
                    "description"
                ],
                severity=item.get(
                    "severity"
                ),
            )
        )

        saved_comparisons.append(
            {
                "id": contradiction.id,
                "finding_a_id": (
                    contradiction.finding_a_id
                ),
                "finding_b_id": (
                    contradiction.finding_b_id
                ),
                "comparison_type": (
                    contradiction.comparison_type
                ),
                "description": (
                    contradiction.description
                ),
                "severity": (
                    contradiction.severity
                ),
            }
        )

    # --------------------------------------------------
    # UPDATE FINDING CONFIDENCE
    # --------------------------------------------------

    for finding in findings:

        # Count how many actual contradictions
        # involve this finding.
        contradiction_count = sum(
            1
            for comparison
            in saved_comparisons
            if comparison["comparison_type"]
            == "contradiction"
            and (
                comparison["finding_a_id"]
                == finding.id
                or
                comparison["finding_b_id"]
                == finding.id
            )
        )

        # Original confidence from Groq
        original_confidence = (
            finding.confidence
            if finding.confidence is not None
            else 0.0
        )

        # Adjust confidence based on
        # contradiction count.
        finding.confidence = (
            adjust_confidence(
                original_confidence,
                contradiction_count,
            )
        )

    # Save updated confidence values
    db.commit()

    # --------------------------------------------------

    return {
        "session_id": session_id,
        "comparisons": saved_comparisons,
    }