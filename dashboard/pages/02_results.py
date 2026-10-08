"""
Results page: overall score, RAG-flagged dimension scores, radar chart
against the selected sector benchmark, and top gaps with recommended
actions.
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))
from common import (  # noqa: E402
    build_p9_link,
    get_questions_data,
    init_session_state,
    render_sidebar,
    total_question_count,
)

import scoring  # noqa: E402
from charts import build_radar_chart  # noqa: E402

st.set_page_config(page_title="Results", page_icon="\U0001F4CA", layout="wide")

RAG_COLOUR = {"red": "red", "amber": "orange", "green": "green"}


def main() -> None:
    questions_data = get_questions_data()
    init_session_state()
    render_sidebar()

    st.title("Results")

    total = total_question_count(questions_data)
    if len(st.session_state.answers) < total:
        st.info("Answer every question on the Assessment page to see your results.")
        return

    result = scoring.score_all(st.session_state.answers)
    dimension_scores = result["dimension_scores"]
    overall = result["overall_score"]
    label = scoring.maturity_label(overall)
    sector = st.session_state.sector
    benchmark_scores = scoring.get_benchmark_scores(sector)
    gaps = scoring.rank_gaps(dimension_scores, benchmark_scores, top_n=5)

    overall_colour = RAG_COLOUR[scoring.rag_band(overall)]
    st.markdown(f"## Overall maturity: :{overall_colour}[{overall} out of 5], {label}")

    col1, col2, col3 = st.columns(3)
    col1.metric("Overall score", f"{overall} / 5", label)
    weakest = min(dimension_scores, key=dimension_scores.get)
    col2.metric("Weakest dimension", weakest, f"{dimension_scores[weakest]} / 5")
    strongest = max(dimension_scores, key=dimension_scores.get)
    col3.metric("Strongest dimension", strongest, f"{dimension_scores[strongest]} / 5")

    fig = build_radar_chart(dimension_scores, benchmark_scores, sector)
    st.plotly_chart(fig, width="stretch")
    st.caption(
        "Source: self-reported assessment scores against the CMMI Data Management "
        f"Maturity model's 5 dimensions. {sector} benchmark figures are drawn from "
        "data/benchmarks.csv."
    )

    st.markdown("### Scores by dimension")
    st.caption("Colour flags where the risk actually sits, not just the raw number.")
    for dimension, score in dimension_scores.items():
        colour = RAG_COLOUR[scoring.rag_band(score)]
        st.markdown(f"**{dimension}**: :{colour}[{score} / 5]")

    st.markdown("### Your top gaps")
    for gap in gaps:
        colour = RAG_COLOUR[scoring.rag_band(gap["org_score"])]
        st.markdown(
            f"**{gap['dimension']}**: scoring :{colour}[{gap['org_score']}] against a "
            f"{gap['target_score']} target, a gap of {gap['gap']}."
        )
        for action in gap["recommended_actions"]:
            st.markdown(f"- {action}")

    st.info("Go to the Report page to download a PDF gap analysis report.")

    st.divider()
    p9_link = build_p9_link(st.session_state.org_name, sector)
    if overall_colour == "red":
        st.markdown(
            "### Before AI governance, fix the foundation\n"
            "An AI governance structure only works if the data underneath it "
            "is trustworthy. With a score this low, that is the priority. "
            f"Once the dimensions above are in better shape, the "
            f"[AI Governance Readiness Assessment]({p9_link}) scores whether "
            "you are ready to govern AI systems built on top of it."
        )
    else:
        st.markdown(
            "### Next: AI governance readiness\n"
            "This assessment scores your data foundation. The companion "
            f"[AI Governance Readiness Assessment]({p9_link}) scores whether "
            "you are ready to govern AI systems built on that foundation, "
            "the next question once the data underneath it can be trusted."
        )


if __name__ == "__main__":
    main()
