import os

from dotenv import load_dotenv


load_dotenv()


class Settings:

    APP_NAME: str = os.getenv(
        "APP_NAME",
        "Enterprise Research Intelligence Agent"
    )

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./data/research.db"
    )

    GROQ_API_KEY: str = os.getenv(
        "GROQ_API_KEY",
        ""
    )

    GROQ_MODEL: str = os.getenv(
        "GROQ_MODEL",
        "llama-3.3-70b-versatile"
    )


settings = Settings()