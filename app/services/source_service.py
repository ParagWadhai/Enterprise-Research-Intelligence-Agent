from app.research.search import search_web
from app.research.collector import collect_page
from app.research.source_quality import (
    calculate_source_quality,
)
from app.research.utils import normalize_url

from app.database.repository import (
    source_exists,
    create_source,
)


def collect_sources_for_question(
    db,
    session_id: int,
    research_question: str,
    max_results: int = 5,
):

    search_results = search_web(
        research_question,
        max_results=max_results,
    )

    collected_sources = []

    for result in search_results:

        url = result.get("url")

        if not url:
            continue

        normalized_url = normalize_url(url)

        if source_exists(
            db,
            normalized_url
        ):
            continue

        content = collect_page(
            normalized_url
        )

        if not content:
            continue

        quality_score = (
            calculate_source_quality(
                normalized_url
            )
        )

        source = create_source(
            db=db,
            session_id=session_id,
            title=result.get(
                "title",
                "Untitled Source"
            ),
            url=normalized_url,
            content=content,
            quality_score=quality_score,
        )

        collected_sources.append(source)

    return collected_sources