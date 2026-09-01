from app.database.database import SessionLocal
from app.database.models import ResearchSession


def test_create_research_session():

    db = SessionLocal()

    session = ResearchSession(
        question="How is AI transforming retail operations?",
        status="created"
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    assert session.id is not None
    assert session.question == "How is AI transforming retail operations?"

    db.delete(session)
    db.commit()

    db.close()