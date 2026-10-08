"""
Data Maturity Assessment Tool: Streamlit entry page.

Introduces the 5-dimension assessment, collects organisation name and
sector for benchmarking, and hands off to the Assessment page.
"""

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent))
from common import get_questions_data, init_session_state, render_sidebar  # noqa: E402

st.set_page_config(
    page_title="Data Maturity Assessment",
    page_icon="\U0001F4CA",
    layout="wide",
    initial_sidebar_state="expanded",
)


def main() -> None:
    questions_data = get_questions_data()
    init_session_state()
    render_sidebar()

    st.title("Data Maturity Assessment")
    st.caption(
        "A scored, benchmarked view of where your organisation stands across "
        "5 data dimensions before any strategy conversation starts."
    )

    dimension_names = ", ".join(d["name"] for d in questions_data["dimensions"])
    st.markdown(
        f"This assessment covers 25 questions across 5 dimensions: {dimension_names}. "
        "Each question is scored 1 to 5 against the CMMI Data Management Maturity "
        "model, from Ad Hoc to Optimising."
    )

    st.markdown("### How it works")
    st.markdown(
        "1. Enter your organisation name and sector in the sidebar.\n"
        "2. Answer all 25 questions on the Assessment page.\n"
        "3. See your scored radar chart against a sector benchmark on the Results page.\n"
        "4. Download a PDF gap analysis report with prioritised recommendations."
    )

    st.info("Use the sidebar navigation to move to the Assessment page.")


if __name__ == "__main__":
    main()
