from app.agents.state import ResearchState

from app.services.research_execution import (
    execute_source_collection,
)

from app.services.knowledge_service import (
    build_knowledge_base,
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

from app.services.research_status import (
    update_research_status,
)


def run_research_pipeline(
    db,
    session_id: int,
    research_question: str,
):

    print(
        f"\n🚀 RESEARCH PIPELINE STARTED "
        f"session={session_id}"
    )

    state = ResearchState(
        session_id=session_id,
        research_question=research_question,
    )

    result = {
        "session_id": session_id,
        "question": research_question,
        "stages": {},
    }

    try:

        # =================================================
        # Stage 1: Collect Sources
        # =================================================

        state.status = "collecting_sources"

        update_research_status(
            db=db,
            session_id=session_id,
            status="collecting_sources",
            progress=20,
            current_stage="Collecting sources",
        )

        print(
            "🔎 Stage 1: Collecting sources..."
        )

        source_result = execute_source_collection(
            db=db,
            session_id=session_id,
        )

        result["stages"][
            "source_collection"
        ] = source_result

        print(
            "✅ Stage 1 completed."
        )


        # =================================================
        # Stage 2: Build Knowledge Base
        # =================================================

        state.status = "building_knowledge"

        update_research_status(
            db=db,
            session_id=session_id,
            status="building_knowledge",
            progress=40,
            current_stage="Building knowledge base",
        )

        print(
            "📚 Stage 2: Building knowledge base..."
        )

        knowledge_result = build_knowledge_base(
            db=db,
            session_id=session_id,
        )

        result["stages"][
            "knowledge_base"
        ] = knowledge_result

        print(
            "✅ Stage 2 completed."
        )


        # =================================================
        # Stage 3: Analyze Evidence
        # =================================================

        state.status = "analyzing_evidence"

        update_research_status(
            db=db,
            session_id=session_id,
            status="analyzing_evidence",
            progress=60,
            current_stage="Analyzing evidence",
        )

        print(
            "🧠 Stage 3: Analyzing evidence..."
        )

        analysis_result = analyze_research_question(
            db=db,
            session_id=session_id,
            query=research_question,
            top_k=4,
        )

        result["stages"][
            "analysis"
        ] = analysis_result

        print(
            "✅ Stage 3 completed."
        )


        # =================================================
        # Stage 4: Compare Evidence
        # =================================================

        state.status = "comparing_evidence"

        update_research_status(
            db=db,
            session_id=session_id,
            status="comparing_evidence",
            progress=75,
            current_stage="Comparing evidence",
        )

        print(
            "⚖️ Stage 4: Comparing evidence..."
        )

        comparison_result = (
            compare_session_findings(
                db=db,
                session_id=session_id,
            )
        )

        result["stages"][
            "comparison"
        ] = comparison_result

        print(
            "✅ Stage 4 completed."
        )


        # =================================================
        # Stage 5: Generate Conclusion
        # =================================================

        state.status = "synthesizing"

        update_research_status(
            db=db,
            session_id=session_id,
            status="synthesizing",
            progress=90,
            current_stage="Generating conclusion",
        )

        print(
            "📝 Stage 5: Generating conclusion..."
        )

        conclusion_result = (
            generate_research_conclusion(
                db=db,
                session_id=session_id,
            )
        )

        result["stages"][
            "synthesis"
        ] = conclusion_result

        print(
            "✅ Stage 5 completed."
        )


        # =================================================
        # Pipeline Completed
        # =================================================

        state.status = "completed"

        update_research_status(
            db=db,
            session_id=session_id,
            status="completed",
            progress=100,
            current_stage="Research completed",
        )

        result["status"] = "completed"

        result["report"] = (
            conclusion_result
        )

        print(
            f"\n✅ RESEARCH PIPELINE COMPLETED "
            f"session={session_id}\n"
        )

        return result


    except Exception as exc:

        # =================================================
        # Pipeline Failed
        # =================================================

        state.status = "failed"

        state.error = str(exc)

        print(
            f"\n❌ RESEARCH PIPELINE FAILED "
            f"session={session_id}"
        )

        print(
            f"Error: {exc}\n"
        )

        # ---------------------------------------------
        # Try to persist failure status
        # ---------------------------------------------

        try:

            update_research_status(
                db=db,
                session_id=session_id,
                status="failed",
                progress=0,
                current_stage="Research failed",
                error_message=str(exc),
            )

        except Exception as status_error:

            print(
                "⚠️ Could not update failure status:"
            )

            print(
                status_error
            )


        return {
            "status": "failed",
            "session_id": session_id,
            "question": research_question,
            "error": str(exc),
        }