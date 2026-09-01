from app.ai.llm import generate_response


def test_groq_connection():

    response = generate_response(
        system_prompt=(
            "You are a helpful enterprise research assistant."
        ),
        user_prompt=(
            "Explain AI transformation in retail "
            "in one sentence."
        ),
    )

    assert response
    assert isinstance(response, str)

    print("\nGroq response:")
    print(response)