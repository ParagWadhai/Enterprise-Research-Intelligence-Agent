from sqlalchemy.orm import Session

from app.database.repository import (
    create_research_session,
    get_research_session,
    create_research_question,
)

from app.research.planner import (
    create_research_plan,
)


def start_research(
    db: Session,
    question: str,
):

    session = create_research_session(
        db=db,
        question=question,
    )

    plan = create_research_plan(
        question=question,
    )

    for item in plan["research_questions"]:

        create_research_question(
            db=db,
            session_id=session.id,
            question=item["question"],
            category=item["category"],
        )

    session.status = "planned"

    db.commit()
    db.refresh(session)

    return session


def get_research(
    db: Session,
    session_id: int,
):

    return get_research_session(
        db=db,
        session_id=session_id,
    )