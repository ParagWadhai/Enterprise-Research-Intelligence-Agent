import json
from typing import Literal

from pydantic import BaseModel

from app.ai.llm import generate_response


# =========================================================
# Pydantic schemas
# =========================================================

class ResearchQuestion(BaseModel):

    question: str

    category: Literal[
        "technology",
        "benefits",
        "adoption",
        "risks",
        "future_trends",
    ]

    model_config = {
        "extra": "forbid"
    }


class ResearchPlanResponse(BaseModel):

    research_questions: list[ResearchQuestion]

    model_config = {
        "extra": "forbid"
    }


# =========================================================
# System prompt
# =========================================================

SYSTEM_PROMPT = """
You are an enterprise research planning assistant.

Your job is to convert a broad business research question
into a structured research plan.

Do NOT answer the research question.

Instead, identify the specific questions that must be researched
before a reliable conclusion can be generated.

The research plan must cover these five areas:

1. Technology
   - What technologies or AI capabilities are being used?

2. Benefits
   - What measurable business benefits or outcomes are reported?

3. Adoption
   - How widely are these technologies being adopted?
   - What implementation approaches are being used?

4. Risks
   - What technical, organizational, data, privacy, security,
     or regulatory challenges exist?

5. Future Trends
   - What emerging technologies or future developments are expected?

IMPORTANT:

- Generate EXACTLY 5 research questions.
- Generate ONE question for each category.
- Do not create additional questions.
- Do not combine multiple categories into one question.
- Avoid overlapping questions.
- Questions must be specific and researchable.
- Questions should help produce an evidence-based enterprise report.
- Do NOT answer the questions.
"""


# =========================================================
# Create research plan
# =========================================================

def create_research_plan(
    question: str,
) -> dict:

    user_prompt = f"""
Research Question:

{question}

Create a research plan containing EXACTLY 5 questions.

The five questions MUST use these categories:

1. technology
2. benefits
3. adoption
4. risks
5. future_trends

Return ONLY the requested structured output.
"""


    response = generate_response(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=user_prompt,
        response_schema=ResearchPlanResponse,
    )


    # =====================================================
    # Parse structured response
    # =====================================================

    try:

        result = json.loads(response)

    except json.JSONDecodeError as exc:

        raise ValueError(
            "Groq returned invalid JSON for research plan."
        ) from exc


    # =====================================================
    # Validate schema
    # =====================================================

    validated = (
        ResearchPlanResponse.model_validate(
            result
        )
    )


    # =====================================================
    # Safety check
    # =====================================================

    if len(validated.research_questions) != 5:

        raise ValueError(
            "Research planner must generate exactly "
            "5 research questions."
        )


    return validated.model_dump()