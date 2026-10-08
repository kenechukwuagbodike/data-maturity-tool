"""
Shared radar chart builder for the assessment tool, used by both the
Streamlit dashboard and the PDF report so the two never drift apart
visually.
"""

import plotly.graph_objects as go

NAVY = "#14213D"
GREY = "#CCCCCC"
DARK = "#1A1A1A"


def _biggest_gap_annotation(dimension_scores: dict, benchmark_scores: dict) -> str:
    """
    An action title, not a descriptive label: names the org's actual
    biggest gap instead of a generic "maturity profile" caption.
    """
    if not benchmark_scores:
        weakest = min(dimension_scores, key=dimension_scores.get)
        return f"{weakest} is your weakest dimension, scoring {dimension_scores[weakest]:.1f} out of 5"

    gaps = {d: benchmark_scores.get(d, 0) - score for d, score in dimension_scores.items()}
    biggest = max(gaps, key=gaps.get)
    return (
        f"{biggest} is your biggest gap, scoring {dimension_scores[biggest]:.1f} "
        f"against a {benchmark_scores.get(biggest, 0):.1f} sector reference"
    )


def build_radar_chart(dimension_scores: dict, benchmark_scores: dict, sector: str) -> go.Figure:
    dimensions = list(dimension_scores.keys())
    org_values = [dimension_scores[d] for d in dimensions]
    bench_values = [benchmark_scores.get(d, 0) for d in dimensions]

    dims_closed = dimensions + [dimensions[0]]
    org_closed = org_values + [org_values[0]]
    bench_closed = bench_values + [bench_values[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=bench_closed,
        theta=dims_closed,
        name=f"{sector} benchmark",
        line=dict(color=GREY, dash="dot"),
        fill="none",
    ))
    fig.add_trace(go.Scatterpolar(
        r=org_closed,
        theta=dims_closed,
        name="Your organisation",
        line=dict(color=NAVY, width=3),
        fill="toself",
        fillcolor="rgba(20, 33, 61, 0.15)",
    ))
    fig.update_layout(
        polar=dict(
            domain=dict(y=[0, 0.80]),
            radialaxis=dict(visible=True, range=[0, 5], gridcolor="#EEEEEE"),
            angularaxis=dict(linecolor=GREY),
        ),
        showlegend=True,
        legend=dict(orientation="h", yanchor="top", y=0.93, xanchor="right", x=1),
        margin=dict(t=20, b=30, l=40, r=40),
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family="Inter, Arial, sans-serif", size=12, color=DARK),
    )
    fig.add_annotation(
        text=_biggest_gap_annotation(dimension_scores, benchmark_scores),
        xref="paper", yref="paper",
        x=0, y=0.99,
        xanchor="left", yanchor="top",
        showarrow=False,
        font=dict(size=14, color=NAVY, family="Inter, Arial, sans-serif"),
    )
    return fig
