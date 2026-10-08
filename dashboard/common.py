"""
Shared session state, sidebar inputs, and data loaders for the Data
Maturity Assessment Streamlit app. Imported by app.py and every page in
dashboard/pages/ so questions, benchmarks, and the organisation's answers
stay in sync across pages.
"""

import sys
from pathlib import Path
from urllib.parse import urlencode

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent / "assessment"))
import scoring  # noqa: E402

P9_APP_URL = "https://keni-ai-governance-framework.streamlit.app"

# P9 and P10 score different sector benchmark sets with different naming.
# Maps a P10 sector onto its closest P9 equivalent so a cross-link can
# pre-fill the other tool's sector selector. P10's SME / General has no
# P9 counterpart and is left unmapped: P9 defaults on its own in that case.
SECTOR_MAP_P10_TO_P9 = {
    "NHS / Public Sector": "Healthcare / NHS",
    "Financial Services": "Financial Services",
    "Retail / E-commerce": "Retail / E-commerce",
}


@st.cache_data
def get_questions_data() -> dict:
    return scoring.load_questions()


@st.cache_data
def get_benchmark_sectors() -> list[str]:
    return scoring.load_benchmarks()["sector"].tolist()


def init_session_state() -> None:
    if "answers" not in st.session_state:
        st.session_state.answers = {}
    if "org_name" not in st.session_state:
        st.session_state.org_name = st.query_params.get("org", "")
    if "sector" not in st.session_state:
        sectors = get_benchmark_sectors()
        incoming = st.query_params.get("sector", "")
        st.session_state.sector = incoming if incoming in sectors else sectors[0]


def build_p9_link(org_name: str, sector: str) -> str:
    params = {}
    if org_name:
        params["org"] = org_name
    mapped_sector = SECTOR_MAP_P10_TO_P9.get(sector)
    if mapped_sector:
        params["sector"] = mapped_sector
    query = f"?{urlencode(params)}" if params else ""
    return f"{P9_APP_URL}{query}"


def render_sidebar() -> None:
    st.sidebar.header("Your details")
    st.session_state.org_name = st.sidebar.text_input(
        "Organisation name (for your report)", value=st.session_state.org_name
    )
    sectors = get_benchmark_sectors()
    st.session_state.sector = st.sidebar.selectbox(
        "Compare against sector", sectors, index=sectors.index(st.session_state.sector)
    )


def total_question_count(questions_data: dict) -> int:
    return sum(len(d["questions"]) for d in questions_data["dimensions"])
