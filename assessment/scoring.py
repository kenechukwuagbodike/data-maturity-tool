"""
Maturity scoring for the data maturity self-assessment.

Loads questions.json, scores an organisation's answers per dimension,
looks up a sector benchmark from data/benchmarks.csv, and ranks gaps
for the PDF report and the dashboard's radar chart.
"""

import json
import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent
QUESTIONS_PATH = BASE_DIR / "questions.json"
BENCHMARKS_PATH = BASE_DIR.parent / "data" / "benchmarks.csv"
RECOMMENDATIONS_PATH = BASE_DIR.parent / "data" / "recommendations.json"

DEFAULT_TARGET_SCORE = 4.0  # "Managed" on the 1-5 maturity scale

# Shared RAG thresholds so the dashboard and the PDF report never disagree
# about what counts as a risk.
RAG_THRESHOLDS = {"red": 2.5, "amber": 3.5}  # amber if red_threshold <= score < amber_threshold


def rag_band(score: float) -> str:
    if score < RAG_THRESHOLDS["red"]:
        return "red"
    if score < RAG_THRESHOLDS["amber"]:
        return "amber"
    return "green"


def load_questions() -> dict:
    with QUESTIONS_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def load_benchmarks() -> pd.DataFrame:
    return pd.read_csv(BENCHMARKS_PATH)


def load_recommendations() -> dict:
    with RECOMMENDATIONS_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def score_dimension(dimension: dict, answers: dict[str, int]) -> float:
    question_ids = [q["id"] for q in dimension["questions"]]
    scores = [answers[qid] for qid in question_ids if qid in answers]
    if not scores:
        return 0.0
    return round(sum(scores) / len(scores), 2)


def score_all(answers: dict[str, int]) -> dict:
    """
    answers: {question_id: score 1-5}, expects all 25 ids present for a
    complete assessment, but scores whatever subset is given.
    """
    questions_data = load_questions()
    dimension_scores = {}
    for dimension in questions_data["dimensions"]:
        dimension_scores[dimension["name"]] = score_dimension(dimension, answers)

    overall = round(sum(dimension_scores.values()) / len(dimension_scores), 2) if dimension_scores else 0.0

    return {
        "dimension_scores": dimension_scores,
        "overall_score": overall,
    }


def maturity_label(score: float) -> str:
    questions_data = load_questions()
    levels = questions_data["maturity_levels"]
    nearest = min(levels.keys(), key=lambda level: abs(int(level) - round(score)))
    return levels[nearest]


def get_benchmark_scores(sector: str) -> dict[str, float]:
    benchmarks = load_benchmarks()
    sector_row = benchmarks[benchmarks["sector"] == sector]
    if sector_row.empty:
        logger.warning("No benchmark found for sector %s, returning empty benchmark", sector)
        return {}
    row = sector_row.iloc[0]
    dimension_columns = [c for c in benchmarks.columns if c != "sector"]
    return {col: float(row[col]) for col in dimension_columns}


def rank_gaps(dimension_scores: dict[str, float], benchmark_scores: dict[str, float] | None = None,
              top_n: int = 5) -> list[dict]:
    """
    Ranks dimensions by how far the org sits below either its sector
    benchmark, when one is available, or the fixed "managed" target
    otherwise. Largest gap first. Attaches recommended actions per gap.
    """
    recommendations = load_recommendations()
    gaps = []
    for dimension_name, org_score in dimension_scores.items():
        target = benchmark_scores.get(dimension_name) if benchmark_scores else None
        target = target if target is not None else DEFAULT_TARGET_SCORE
        gap_size = round(target - org_score, 2)
        gaps.append({
            "dimension": dimension_name,
            "org_score": org_score,
            "target_score": target,
            "gap": gap_size,
            "recommended_actions": recommendations.get(dimension_name, []),
        })
    gaps.sort(key=lambda g: g["gap"], reverse=True)
    return gaps[:top_n]
