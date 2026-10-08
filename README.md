# Data Maturity Assessment Tool

> A 25-question self-assessment that scores an organisation's data foundation
> across 5 dimensions, benchmarks it against sector peers, and generates a
> PDF gap analysis with prioritised recommendations.

Part of the [Data to Decisions](https://github.com/kenechukwuagbodike) portfolio by
Kene Agbodike, Data and AI Decision Systems Consultant.

---

## Overview

No organisation benefits from AI if its data foundations are weak, and most
leaders asking about AI strategy have never had that foundation scored. This
tool answers that question first: 25 questions across 5 dimensions, scored 1
to 5 against CMMI Data Management Maturity level anchors (Ad Hoc through
Optimising), each with concrete, not abstract, descriptions of what each
score actually looks like in practice.

The assessment produces:

1. A **Plotly radar chart** comparing the organisation's score against a
   sector benchmark (NHS/Public Sector, Financial Services, Retail/E-commerce,
   or SME/General).
2. A **RAG-flagged scores table** across all 5 dimensions, so risk is visible
   at a glance, not just the raw numbers.
3. A **downloadable PDF gap analysis report**, built with the same radar
   chart as the dashboard, covering the organisation's top gaps, each with a
   dimension-specific explanation of why it matters and 3 recommended
   actions.

The framework is derived from four source documents, not from data: CMMI's
Data Management Maturity (DMM) Model, DAMA-DMBOK Second Edition, Gartner's
Enterprise Information Management Maturity Model, and the NHS Data Strategy.
Each source was individually verified against its own title or contents
page before being cited, and two citation discrepancies were caught and
corrected during that process rather than assumed correct from the brief.

Pairs with [AI Governance Framework](https://github.com/kenechukwuagbodike/ai-governance-framework):
that tool is prescriptive (the governance structure to adopt once AI is in
scope), this one is diagnostic (whether the data foundation underneath it
can support that structure at all). The two are companion assessments, not
a bundled product: a results page links across once the data foundation
scores well enough to make AI governance a live question, not an inherited
one.

## Stack

`Python · Streamlit · ReportLab · Plotly · pandas`

## Demo

- **Live demo:** _deploying_
- **Companion tool:** https://keni-ai-governance-framework.streamlit.app/

## Getting started

```bash
# Clone the repo
git clone https://github.com/kenechukwuagbodike/data-maturity-tool.git
cd data-maturity-tool

# Create virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1      # Windows PowerShell
# source .venv/bin/activate       # macOS / Linux

# Install dependencies
pip install -r requirements.txt
```

## Project structure

```
data-maturity-tool/
├── dashboard/       Streamlit app: intro, assessment, results, report pages
├── assessment/      Question bank, scoring logic, radar chart, PDF generator
├── data/            Sector benchmarks, recommended actions
├── requirements.txt
└── README.md
```

## Running the dashboard

```bash
streamlit run dashboard/app.py
```

## About

**Kene Agbodike**, Data and AI Decision Systems Consultant

Certifications: Microsoft Fabric Data Engineer Associate, Fabric Analytics
Engineer Associate, Azure Solutions Architect Expert, Azure AI Engineer,
Azure Data Scientist

[GitHub](https://github.com/kenechukwuagbodike) · [Upwork](https://www.upwork.com/freelancers/~01ffe0a90179159b67)
