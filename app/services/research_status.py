from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.database.models import ResearchSession


def update_research_status(
    db: Session,
    session_id: int,
    status: str,
    progress: int,
    current_stage: str,
    error_message: str | None = None,
):

    research_session = (
        db.query(ResearchSession)
        .filter(
            ResearchSession.id == session_id
        )
        .first()
    )

    if research_session is None:
        return

    research_session.status = status

    research_session.progress = progress

    research_session.current_stage = (
        current_stage
    )

    research_session.error_message = (
        error_message
    )

    if status == "completed":

        research_session.completed_at = (
            datetime.now(timezone.utc)
        )

    db.commit()