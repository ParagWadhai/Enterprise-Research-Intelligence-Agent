from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.research import (
    ResearchRequest,
    ResearchResponse,
    ResearchQuestionResponse,
)
from fastapi import (
    BackgroundTasks,
)
from app.services.research_service import (
    start_research,
    get_research,
)
from app.services.research_execution import (
    execute_source_collection,
)
from app.services.knowledge_service import (
    build_knowledge_base,
)
from app.retrieval.retriever import (
    retrieve_chunks,
)
from app.services.analysis_service import (
    analyze_research_question,
)
from app.services.comparison_service import (
    compare_session_findings,
)
from app.services.synthesis_service import (
    generate_research_conclusion,
)
from app.services.research_orchestrator import (
    run_research_pipeline,
)

router = APIRouter(
    prefix="/api/v1/research",
    tags=["Research"]
)


@router.post(
    "",
    response_model=ResearchResponse
)
def create_research(
    request: ResearchRequest,
    db: Session = Depends(get_db)
):

    research_session = start_research(
        db=db,
        question=request.question,
    )

    return ResearchResponse(
        session_id=research_session.id,
        question=research_session.question,
        status=research_session.status,
        progress=research_session.progress,
        current_stage=research_session.current_stage,
        error_message=research_session.error_message,
        created_at=research_session.created_at,

        research_questions=[
            ResearchQuestionResponse(
                id=item.id,
                question=item.question,
                category=item.category,
                status=item.status,
            )
            for item in research_session.research_questions
        ],
    )

@router.post(
    "/{session_id}/collect-sources"
)
def collect_sources(
    session_id: int,
    db: Session = Depends(get_db),
):

    result = execute_source_collection(
        db=db,
        session_id=session_id,
    )

    return result

@router.get(
    "/{session_id}",
    response_model=ResearchResponse
)
def get_research_session(
    session_id: int,
    db: Session = Depends(get_db)
):

    research_session = get_research(
        db=db,
        session_id=session_id
    )

    if research_session is None:
        raise HTTPException(
            status_code=404,
            detail="Research session not found"
        )

    return ResearchResponse(
        session_id=research_session.id,
        question=research_session.question,
        status=research_session.status,
        created_at=research_session.created_at,

        research_questions=[
            ResearchQuestionResponse(
                id=item.id,
                question=item.question,
                category=item.category,
                status=item.status,
            )
            for item in research_session.research_questions
        ],
    )

@router.post(
    "/{session_id}/build-knowledge"
)
def build_knowledge(
    session_id: int,
    db: Session = Depends(get_db),
):

    result = build_knowledge_base(
        db=db,
        session_id=session_id,
    )

    return result

@router.get(
    "/{session_id}/search"
)
def search_knowledge(
    session_id: int,
    query: str,
    top_k: int = 5,
    db: Session = Depends(get_db),
):

    results = retrieve_chunks(
        db=db,
        query=query,
        top_k=top_k,
    )

    return {
        "session_id": session_id,
        "query": query,
        "results": results,
    }

@router.post(
    "/{session_id}/analyze"
)
def analyze_research(
    session_id: int,
    query: str,
    top_k: int = 8,
    db: Session = Depends(get_db),
):

    result = analyze_research_question(
        db=db,
        session_id=session_id,
        query=query,
        top_k=top_k,
    )

    return result

@router.post(
    "/{session_id}/compare"
)
def compare_research(
    session_id: int,
    db: Session = Depends(get_db),
):

    result = compare_session_findings(
        db=db,
        session_id=session_id,
    )

    return result

@router.post(
    "/{session_id}/synthesize"
)
def synthesize_research_report(
    session_id: int,
    db: Session = Depends(get_db),
):

    result = generate_research_conclusion(
        db=db,
        session_id=session_id,
    )

    return result

@router.post(
    "/{session_id}/run"
)
def run_research(
    session_id: int,
    query: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):

    background_tasks.add_task(
        run_research_pipeline,
        db,
        session_id,
        query,
    )

    return {
        "session_id": session_id,
        "status": "started",
        "message": (
            "Research pipeline started."
        ),
    }