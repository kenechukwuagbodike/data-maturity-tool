# P10: Data Maturity Assessment Tool

## What this project does
A Streamlit self-assessment tool for organisations starting a data or AI
programme. 25 questions across 5 dimensions (Data Infrastructure, Data
Quality and Governance, Analytics and Reporting, AI and ML Readiness, Data
Culture and Skills), scored 1-5 and aligned to CMMI Data Management Maturity
levels (Ad Hoc to Optimising). Produces a Plotly radar chart against a
sector benchmark and a ReportLab PDF gap analysis report with prioritised
recommendations.

This project does not use a training dataset. There is no model to build.
The framework is derived from CMMI DMM, DAMA DMBOK v2, the Gartner Data
Management Maturity Model, and the NHS Data Strategy (2021), not from data.

It pairs with [P9: AI Governance Framework](../ai-governance-framework).
P9 is prescriptive (governance structure to adopt); P10 is diagnostic
(readiness score before that structure is built). Keep that distinction
in any copy that presents them together.

## Folder structure
```
data-maturity-tool/
├── dashboard/
│   ├── app.py                  Streamlit: intro page, org name and sector input
│   └── pages/
│       ├── 01_assessment.py    25 questions, 5 per dimension, session_state
│       ├── 02_results.py       Plotly radar chart, scores table, top gaps
│       └── 03_report.py        PDF download page
├── assessment/
│   ├── questions.json          25 questions, 5 dimensions, CMMI-aligned level anchors
│   ├── scoring.py               Score computation, benchmark lookup, gap ranking
│   └── report_generator.py     ReportLab: PDF gap analysis report
├── data/
│   ├── benchmarks.csv          Sector benchmarks (NHS/Financial Services/Retail/SME)
│   └── recommendations.json    3 recommended actions per dimension gap
├── requirements.txt
├── CLAUDE.md
├── PROJECT.md
└── README.md
```

## The 5 dimensions
1. Data Infrastructure
2. Data Quality and Governance
3. Analytics and Reporting
4. AI and ML Readiness
5. Data Culture and Skills

Each question carries level_1 (Ad Hoc), level_3 (Defined), and level_5
(Optimising) anchor text so respondents are scoring against a concrete
description, not an abstract number.

## Build order
1. `assessment/questions.json`: 25 questions, 5 per dimension, with CMMI-DMM
   level anchors. Done.
2. `data/recommendations.json`: 3 recommended actions per dimension. Done.
3. `data/benchmarks.csv`: sector benchmark scores per dimension. Done.
4. `assessment/scoring.py`: dimension scores, overall score, gap ranking
   with attached recommendations. Done, unit tested against 3 mock personas.
5. `dashboard/app.py` + `dashboard/pages/`: multi-page Streamlit, session_state
   question tracking, Plotly radar chart (org vs sector benchmark).
6. `assessment/report_generator.py`: ReportLab PDF, embeds the radar chart,
   scores table, top 5 gaps, recommended actions.
7. Deploy to Streamlit Community Cloud. Write README. Commit.

## Writing style (mandatory)
- No em dashes anywhere: not in code comments, dashboard text, insight
  panels, PDF exports, README, or any client-facing copy.
- Use a colon, comma, or rewrite the sentence instead.
- This rule applies to every file generated or edited in this project.

## Session start checklist
1. Read this file
2. Read PROJECT.md: current status, open questions, next actions
3. Activate venv: `.venv\Scripts\Activate.ps1`
4. Check which build step is next in PROJECT.md → Next Actions
5. Build → run → commit
