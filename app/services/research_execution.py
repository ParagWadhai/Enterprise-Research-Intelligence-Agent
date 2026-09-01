from sqlalchemy.orm import Session

from app.database.models import ResearchQuestion

from app.services.source_service import (
    collect_sources_for_question,
)


def execute_source_collection(
    db: Session,
    session_id: int,
):

    questions = (
        db.query(ResearchQuestion)
        .filter(
            ResearchQuestion.session_id
            == session_id
        )
        .all()
    )

    total_sources = 0

    for question in questions:

        sources = collect_sources_for_question(
            db=db,
            session_id=session_id,
            research_question=question.question,
            max_results=5,
        )

        total_sources += len(sources)

        question.status = "researched"

    db.commit()

    return {
        "session_id": session_id,
        "questions_processed": len(questions),
        "sources_collected": total_sources,
    }