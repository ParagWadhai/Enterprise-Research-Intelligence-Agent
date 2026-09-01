import json

from groq import Groq

from app.core.config import settings


# =========================================================
# Groq client
# =========================================================

if not settings.GROQ_API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY is not configured."
    )


client = Groq(
    api_key=settings.GROQ_API_KEY
)


# =========================================================
# Generate response
# =========================================================

def generate_response(
    system_prompt: str,
    user_prompt: str,
    response_schema=None,
) -> str:
    """
    Generate an LLM response.

    If response_schema is provided, Groq Structured Outputs
    with strict JSON Schema will be used.

    Otherwise, normal text generation is used.
    """

    request = {
        "model": settings.GROQ_MODEL,

        "messages": [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],

        "temperature": 0.2,

        "max_completion_tokens": 2048,
    }


    # =====================================================
    # Structured JSON output
    # =====================================================

    if response_schema is not None:

        # ---------------------------------------------
        # Convert Pydantic model → JSON Schema
        # ---------------------------------------------

        schema = (
            response_schema.model_json_schema()
        )

        request["response_format"] = {
            "type": "json_schema",
            "json_schema": {
                "name": (
                    response_schema.__name__.lower()
                ),
                "strict": True,
                "schema": schema,
            },
        }


    # =====================================================
    # Call Groq
    # =====================================================

    response = client.chat.completions.create(
        **request
    )


    message = response.choices[0].message

    content = message.content


    # =====================================================
    # Safety check
    # =====================================================

    if not content:

        raise ValueError(
            "Groq returned an empty response."
        )


    return content