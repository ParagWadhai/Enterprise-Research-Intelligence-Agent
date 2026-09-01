def adjust_confidence(
    original_confidence: float,
    contradiction_count: int,
) -> float:

    if contradiction_count <= 0:
        return original_confidence

    penalty = (
        0.10 * contradiction_count
    )

    adjusted = (
        original_confidence - penalty
    )

    return max(
        0.0,
        round(adjusted, 2)
    )