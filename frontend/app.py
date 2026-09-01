import time

import requests
import streamlit as st


# =========================================================
# Configuration
# =========================================================

API_BASE_URL = "http://127.0.0.1:8000/api/v1"


# =========================================================
# Page configuration
# =========================================================

st.set_page_config(
    page_title="Enterprise Research Intelligence Agent",
    page_icon="🔎",
    layout="wide",
)


# =========================================================
# Custom CSS
# =========================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        font-size: 1rem;
        opacity: 0.7;
        margin-bottom: 2rem;
    }

    .stage-box {
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 8px;
        border: 1px solid #ddd;
    }

    .completed {
        border-left: 5px solid #28a745;
    }

    .running {
        border-left: 5px solid #ff9800;
    }

    .pending {
        border-left: 5px solid #aaa;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# Header
# =========================================================

st.markdown(
    '<div class="main-title">'
    'Enterprise AI Research Intelligence Agent'
    '</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    'Structured, evidence-based enterprise research '
    'with source traceability'
    '</div>',
    unsafe_allow_html=True,
)


# =========================================================
# Research input
# =========================================================

st.subheader("Research Question")

question = st.text_area(
    "Enter a research question",
    placeholder=(
        "Example: How is AI transforming "
        "retail operations?"
    ),
    height=100,
)


# =========================================================
# Start Research
# =========================================================

if st.button(
    "🚀 Start Research",
    type="primary",
    use_container_width=True,
):

    if not question.strip():

        st.warning(
            "Please enter a research question."
        )

        st.stop()

    try:

        # -------------------------------------------------
        # Create research session
        # -------------------------------------------------

        response = requests.post(
            f"{API_BASE_URL}/research",
            json={
                "question": question.strip()
            },
            timeout=30,
        )

        response.raise_for_status()

        session_data = response.json()

        session_id = session_data.get(
            "session_id"
        )

        if not session_id:

            st.error(
                "API did not return a session_id."
            )

            st.stop()

        st.session_state[
            "session_id"
        ] = session_id

        st.session_state[
            "research_started"
        ] = True

        # -------------------------------------------------
        # Start background research pipeline
        # -------------------------------------------------

        run_response = requests.post(
            f"{API_BASE_URL}/research/"
            f"{session_id}/run",
            params={
                "query": question.strip()
            },
            timeout=30,
        )

        run_response.raise_for_status()

        st.success(
            f"Research started — Session {session_id}"
        )

    except requests.RequestException as exc:

        st.error(
            f"Unable to connect to backend: {exc}"
        )

        st.stop()


# =========================================================
# Pipeline Monitoring
# =========================================================

if st.session_state.get(
    "research_started",
    False
):

    session_id = st.session_state[
        "session_id"
    ]

    st.divider()

    st.subheader(
        f"Research Pipeline — Session {session_id}"
    )

    # -----------------------------------------------------
    # Containers
    # -----------------------------------------------------

    status_container = st.empty()

    progress_container = st.empty()

    pipeline_container = st.empty()

    report_container = st.empty()

    # -----------------------------------------------------
    # Pipeline polling
    # -----------------------------------------------------

    while True:

        try:

            response = requests.get(
                f"{API_BASE_URL}/research/"
                f"{session_id}",
                timeout=30,
            )

            response.raise_for_status()

            data = response.json()

        except requests.RequestException as exc:

            status_container.error(
                f"Unable to retrieve research status: {exc}"
            )

            break

        status = data.get(
            "status",
            "unknown"
        )

        progress = data.get(
            "progress",
            0
        )

        current_stage = data.get(
            "current_stage",
            "Waiting..."
        )

        # -------------------------------------------------
        # Status
        # -------------------------------------------------

        if status == "completed":

            status_container.success(
                "✅ Research completed"
            )

        elif status == "failed":

            status_container.error(
                "❌ Research failed"
            )

            error_message = data.get(
                "error_message"
            )

            if error_message:

                st.error(
                    error_message
                )

            break

        else:

            status_container.info(
                f"🔄 {current_stage}"
            )

        # -------------------------------------------------
        # Progress
        # -------------------------------------------------

        progress_container.progress(
            min(
                max(
                    progress,
                    0
                ),
                100
            )
            / 100
        )

        progress_container.caption(
            f"{progress}% — {current_stage}"
        )

        # -------------------------------------------------
        # Pipeline stages
        # -------------------------------------------------

        stages = [
            (
                "Research Planning",
                0,
                [
                    "created",
                    "planned",
                ],
            ),
            (
                "Source Collection",
                20,
                [
                    "collecting_sources",
                ],
            ),
            (
                "Knowledge Base",
                40,
                [
                    "building_knowledge",
                ],
            ),
            (
                "Evidence Analysis",
                60,
                [
                    "analyzing_evidence",
                ],
            ),
            (
                "Evidence Comparison",
                75,
                [
                    "comparing_evidence",
                ],
            ),
            (
                "Final Synthesis",
                90,
                [
                    "synthesizing",
                ],
            ),
            (
                "Completed",
                100,
                [
                    "completed",
                ],
            ),
        ]

        pipeline_html = ""

        for name, stage_progress, statuses in stages:

            if status == "completed":

                css_class = "completed"
                icon = "✅"

            elif status in statuses:

                css_class = "running"
                icon = "🔄"

            elif (
                progress >= stage_progress
                and stage_progress != 100
            ):

                css_class = "completed"
                icon = "✅"

            else:

                css_class = "pending"
                icon = "○"

            pipeline_html += f"""
            <div class="stage-box {css_class}">
                <strong>{icon} {name}</strong>
            </div>
            """

        pipeline_container.markdown(
            pipeline_html,
            unsafe_allow_html=True,
        )

        # -------------------------------------------------
        # Completed
        # -------------------------------------------------

        if status == "completed":

            break

        # -------------------------------------------------
        # Wait before polling again
        # -------------------------------------------------

        time.sleep(2)


    # =====================================================
    # Research Questions
    # =====================================================

    research_questions = data.get(
        "research_questions",
        []
    )

    if research_questions:

        st.divider()

        st.subheader(
            "📋 Research Questions"
        )

        for index, rq in enumerate(
            research_questions,
            start=1,
        ):

            with st.expander(
                f"{index}. {rq.get('question', '')}",
                expanded=False,
            ):

                col1, col2 = st.columns(2)

                with col1:

                    st.write(
                        "**Category:**",
                        rq.get(
                            "category",
                            "N/A"
                        ),
                    )

                with col2:

                    st.write(
                        "**Status:**",
                        rq.get(
                            "status",
                            "N/A"
                        ),
                    )


    # =====================================================
    # Final Report
    # =====================================================

    if status == "completed":

        st.divider()

        st.subheader(
            "📊 Final Research Report"
        )

        try:

            synthesis_response = requests.post(
                f"{API_BASE_URL}/research/"
                f"{session_id}/synthesize",
                timeout=120,
            )

            synthesis_response.raise_for_status()

            report = synthesis_response.json()

        except requests.RequestException as exc:

            st.error(
                f"Unable to retrieve final report: {exc}"
            )

            report = None

        if report:

            # ---------------------------------------------
            # Executive Summary
            # ---------------------------------------------

            st.markdown(
                "### Executive Summary"
            )

            st.write(
                report.get(
                    "executive_summary",
                    "No summary available."
                )
            )

            # ---------------------------------------------
            # Conclusion
            # ---------------------------------------------

            st.markdown(
                "### Conclusion"
            )

            st.write(
                report.get(
                    "conclusion",
                    "No conclusion available."
                )
            )

            # ---------------------------------------------
            # Reasoning
            # ---------------------------------------------

            with st.expander(
                "🔍 View Reasoning"
            ):

                st.write(
                    report.get(
                        "reasoning",
                        "No reasoning available."
                    )
                )

            # ---------------------------------------------
            # Recommendations
            # ---------------------------------------------

            recommendations = report.get(
                "recommendations",
                []
            )

            if recommendations:

                st.markdown(
                    "### Recommendations"
                )

                for recommendation in recommendations:

                    st.markdown(
                        f"- {recommendation}"
                    )

            # ---------------------------------------------
            # Risks
            # ---------------------------------------------

            risks = report.get(
                "risks",
                []
            )

            if risks:

                st.markdown(
                    "### Risks"
                )

                for risk in risks:

                    st.markdown(
                        f"- {risk}"
                    )

            # ---------------------------------------------
            # Confidence
            # ---------------------------------------------

            confidence = report.get(
                "confidence"
            )

            if confidence is not None:

                st.metric(
                    "Research Confidence",
                    f"{confidence:.0%}",
                )