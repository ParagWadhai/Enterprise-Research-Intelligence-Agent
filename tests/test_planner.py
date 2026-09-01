from app.research.planner import create_research_plan


def test_research_planner():

    result = create_research_plan(
        "How is AI transforming retail operations?"
    )

    assert "research_questions" in result

    assert len(
        result["research_questions"]
    ) > 0

    print("\nResearch Plan:")

    for item in result["research_questions"]:
        print(
            f"- {item['category']}: "
            f"{item['question']}"
        )