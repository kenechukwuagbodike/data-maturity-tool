"""
Assessment page: 25 questions across 5 dimensions, scored 1 to 5 against
CMMI Data Management Maturity level anchors.
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

st.set_page_config(page_title="Assessment", page_icon="\U0001F4CA", layout="wide")


def render_question(question: dict) -> None:
    with st.expander("What does each score mean for this question?"):
        st.write(f"**1 (Ad Hoc)**: {question['level_1']}")
        st.write(f"**3 (Defined)**: {question['level_3']}")
        st.write(f"**5 (Optimising)**: {question['level_5']}")
    key = f"q_{question['id']}"
    default = st.session_state.answers.get(question["id"], 3)
    score = st.slider(question["question"], min_value=1, max_value=5, value=default, key=key)
    st.session_state.answers[question["id"]] = score


def main() -> None:
    questions_data = get_questions_data()
    init_session_state()
    render_sidebar()

    st.title("Assessment")
    st.caption(
        "Answer each question on the 1 to 5 maturity scale. Expand for what "
        "each score looks like in practice."
    )

    for dimension in questions_data["dimensions"]:
        st.markdown(f"### {dimension['number']}. {dimension['name']}")
        for question in dimension["questions"]:
            render_question(question)
        st.divider()

    total = total_question_count(questions_data)
    answered = len(st.session_state.answers)
    st.progress(answered / total, text=f"{answered} of {total} questions answered")
    if answered == total:
        st.success("All questions answered. Go to the Results page to see your score.")


if __name__ == "__main__":
    main()
