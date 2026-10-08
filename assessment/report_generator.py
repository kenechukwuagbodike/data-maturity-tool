"""
ReportLab PDF gap analysis report for the data maturity self-assessment.

Structure follows the workspace's consulting pack convention: state, then
cause and implication, then action, for each top gap, backed by a full
RAG-coloured scores table and the same radar chart shown in the dashboard.

Typography uses ReportLab's built-in Times-Roman family. It ships with
ReportLab itself, so the PDF renders identically everywhere without any
font file dependency, including on the Linux containers Streamlit
Community Cloud deploys to.
"""

import io
import logging
from datetime import date

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image,
)

from charts import build_radar_chart
from scoring import rag_band, get_benchmark_scores

logger = logging.getLogger(__name__)

NAVY = colors.HexColor("#14213D")
GREY = colors.HexColor("#666666")
LIGHT_GREY = colors.HexColor("#EEEEEE")
DARK = colors.HexColor("#1A1A1A")
RAG_COLOURS = {
    "red": colors.HexColor("#B3261E"),
    "amber": colors.HexColor("#B8860B"),
    "green": colors.HexColor("#2E7D32"),
}

HEADING_FONT = "Times-Bold"
BODY_FONT = "Times-Roman"

# The consequence of leaving each dimension's gap unaddressed, drawn from
# the same level_1 to level_5 contrast respondents score themselves
# against in questions.json, so the report's language matches the
# assessment's own.
CAUSE_AND_IMPLICATION = {
    "Data Infrastructure": (
        "A weak score here usually means data still moves by manual export "
        "and copy-paste rather than managed pipelines, with no tested "
        "recovery plan if a critical platform fails. Every other dimension "
        "depends on this one holding up: governance, reporting, and AI work "
        "all assume the underlying platform is there and stays there."
    ),
    "Data Quality and Governance": (
        "Without named data owners and quality checks, problems surface "
        "when a report looks wrong or a client complains, not before. A "
        "number nobody can trace back to its source is a number nobody can "
        "actually be held accountable for."
    ),
    "Analytics and Reporting": (
        "When teams calculate the same metric differently and nobody has "
        "reconciled it, every report becomes a negotiation about whose "
        "numbers are right before it can be a conversation about what to "
        "do next. Dashboards that sit unopened are a sign this is already "
        "happening."
    ),
    "AI and ML Readiness": (
        "Without a defined path from experimentation to production, models "
        "stay in notebooks and never reach the business problem they were "
        "built for. This is usually the dimension furthest behind, because "
        "it depends on the other four being in place first."
    ),
    "Data Culture and Skills": (
        "Without an executive sponsor or basic data literacy outside the "
        "data team, technical improvements in the other dimensions stall "
        "at adoption: the platform, the quality checks, and the dashboards "
        "all exist, but decisions keep getting made without them."
    ),
}


def build_styles() -> dict:
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "ReportTitle", parent=base["Title"], fontName=HEADING_FONT,
            fontSize=22, textColor=NAVY, spaceAfter=4,
        ),
        "subtitle": ParagraphStyle(
            "ReportSubtitle", parent=base["Normal"], fontName=BODY_FONT,
            fontSize=11, textColor=GREY, spaceAfter=16,
        ),
        "h2": ParagraphStyle(
            "ReportH2", parent=base["Heading2"], fontName=HEADING_FONT,
            fontSize=14, textColor=NAVY, spaceBefore=16, spaceAfter=8,
        ),
        "body": ParagraphStyle(
            "ReportBody", parent=base["Normal"], fontName=BODY_FONT,
            fontSize=10, textColor=DARK, leading=14, spaceAfter=8,
            alignment=TA_JUSTIFY,
        ),
        "gap_state": ParagraphStyle(
            "GapState", parent=base["Normal"], fontName=HEADING_FONT,
            fontSize=11, textColor=DARK, spaceBefore=10, spaceAfter=4,
        ),
        "action": ParagraphStyle(
            "Action", parent=base["Normal"], fontName=BODY_FONT,
            fontSize=10, textColor=DARK, leading=14, spaceAfter=2,
            leftIndent=12,
        ),
        "caption": ParagraphStyle(
            "Caption", parent=base["Normal"], fontName=BODY_FONT,
            fontSize=8, textColor=GREY, spaceAfter=4, alignment=TA_JUSTIFY,
        ),
    }


def build_scores_table(dimension_scores: dict, benchmark_scores: dict) -> Table:
    header = ["Dimension", "Your score", "Sector reference", "Gap"]
    rows = [header]
    rag_cells = []  # (row_index, band) for the "Your score" column
    for row_index, (dimension, score) in enumerate(dimension_scores.items(), start=1):
        benchmark = benchmark_scores.get(dimension, 0)
        gap = round(benchmark - score, 2)
        rows.append([dimension, f"{score:.1f}", f"{benchmark:.1f}", f"{gap:+.1f}"])
        rag_cells.append((row_index, rag_band(score)))

    table = Table(rows, colWidths=[8.5 * cm, 2.5 * cm, 3 * cm, 2 * cm])
    style_commands = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), HEADING_FONT),
        ("FONTNAME", (0, 1), (-1, -1), BODY_FONT),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_GREY]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.white),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]
    for row_index, band in rag_cells:
        style_commands.append(("TEXTCOLOR", (1, row_index), (1, row_index), RAG_COLOURS[band]))
        style_commands.append(("FONTNAME", (1, row_index), (1, row_index), HEADING_FONT))
    table.setStyle(TableStyle(style_commands))
    return table


def build_radar_image(dimension_scores: dict, benchmark_scores: dict, sector: str) -> Image:
    fig = build_radar_chart(dimension_scores, benchmark_scores, sector)
    png_bytes = fig.to_image(format="png", width=900, height=600, scale=2)
    return Image(io.BytesIO(png_bytes), width=15 * cm, height=10 * cm)


def generate_report(
    org_name: str,
    sector: str,
    dimension_scores: dict,
    overall_score: float,
    maturity_label: str,
    gaps: list[dict],
) -> bytes:
    styles = build_styles()
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        topMargin=2 * cm, bottomMargin=2 * cm,
        leftMargin=2 * cm, rightMargin=2 * cm,
    )
    benchmark_scores = get_benchmark_scores(sector)

    overall_band = rag_band(overall_score)
    story = []
    story.append(Paragraph("Data Maturity Gap Analysis", styles["title"]))
    story.append(Paragraph(
        f"{org_name}  |  Benchmarked against {sector}  |  {date.today():%d %B %Y}",
        styles["subtitle"],
    ))

    overall_style = ParagraphStyle(
        "OverallScore", parent=styles["h2"], textColor=RAG_COLOURS[overall_band],
    )
    story.append(Paragraph(
        f"Overall maturity: {overall_score:.1f} out of 5, {maturity_label}.",
        overall_style,
    ))
    story.append(Paragraph(
        "This score reflects self-reported answers against the CMMI Data "
        "Management Maturity model's 5 dimensions. It is a starting point "
        "for prioritising data and AI readiness work, not an external audit.",
        styles["body"],
    ))

    story.append(build_radar_image(dimension_scores, benchmark_scores, sector))
    story.append(Paragraph(
        f"Source: self-reported assessment scores. {sector} reference figures "
        "are drawn from data/benchmarks.csv.",
        styles["caption"],
    ))

    story.append(Paragraph("Scores by dimension", styles["h2"]))
    story.append(build_scores_table(dimension_scores, benchmark_scores))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Top gaps and recommended actions", styles["h2"]))
    for gap in gaps:
        dimension = gap["dimension"]
        band = rag_band(gap["org_score"])
        state_style = ParagraphStyle(
            "GapStateBand", parent=styles["gap_state"], textColor=RAG_COLOURS[band],
        )
        story.append(Paragraph(
            f"{dimension}: scoring {gap['org_score']:.1f} against a "
            f"{gap['target_score']:.1f} reference point, a gap of {gap['gap']:.1f}.",
            state_style,
        ))
        cause = CAUSE_AND_IMPLICATION.get(dimension)
        if cause:
            story.append(Paragraph(cause, styles["body"]))
        for action in gap["recommended_actions"]:
            story.append(Paragraph(f"- {action}", styles["action"]))

    story.append(Spacer(1, 16))
    story.append(Paragraph(
        "Framework references: CMMI Data Management Maturity (DMM) Model, "
        "DAMA-DMBOK Second Edition, Gartner's Enterprise Information "
        "Management Maturity Model, NHS Data Strategy (2022).",
        styles["caption"],
    ))

    doc.build(story)
    logger.info("Generated PDF report for %s (%s)", org_name, sector)
    return buffer.getvalue()
