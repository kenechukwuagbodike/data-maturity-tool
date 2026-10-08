"""
Report page: downloads the ReportLab PDF gap analysis report, built from
the same scores and radar chart shown on the Results page.
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))
from common import (  # noqa: E402
    get_questions_data,
    init_session_state,
    render_sidebar,
    total_question_count,
)

import scoring  # noqa: E402
from report_generator import generate_report  # noqa: E402

st.set_page_config(page_title="Report", page_icon="\U0001F4CA", layout="wide")


def main() -> None:
    questions_data = get_questions_data()
    init_session_state()
    render_sidebar()

    st.title("Report")

    total = total_question_count(questions_data)
    if len(st.session_state.answers) < total:
        st.info("Answer every question on the Assessment page to download your report.")
        return

    result = scoring.score_all(st.session_state.answers)
    dimension_scores = result["dimension_scores"]
    overall = result["overall_score"]
    label = scoring.maturity_label(overall)
    sector = st.session_state.sector
    benchmark_scores = scoring.get_benchmark_scores(sector)
    gaps = scoring.rank_gaps(dimension_scores, benchmark_scores, top_n=5)

    org_name = st.session_state.org_name or "Your organisation"
    st.caption(
        f"Generates a PDF gap analysis report for {org_name}, benchmarked "
        f"against {sector}, covering the radar chart, scores table, and top "
        "gaps with recommended actions shown on the Results page."
    )

    pdf_bytes = generate_report(org_name, sector, dimension_scores, overall, label, gaps)
    st.download_button(
        "Download PDF gap analysis report",
        data=pdf_bytes,
        file_name="data_maturity_gap_analysis.pdf",
        mime="application/pdf",
    )


if __name__ == "__main__":
    main()
