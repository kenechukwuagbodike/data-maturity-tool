# Project 10: Data Maturity Assessment Tool
**Status:** Building, Session 3 complete (dashboard + PDF report done, deployment next)
**Last Updated:** 2026-10-03
**Live Demo:** Not yet deployed
**GitHub:** Not yet created

---

## Vision
No organisation benefits from AI if its data foundations are weak. This tool
gives a data or AI leader a scored, benchmarked view of exactly where their
organisation stands across 5 dimensions before any strategy conversation
starts. It is both a consulting entry point (produces a report that
justifies further engagement) and a standalone lead generation asset
(published on Streamlit, shared on LinkedIn, linked from the Upwork profile).

Pairs with [P9: AI Governance Framework](../ai-governance-framework): P9
prescribes the governance structure, P10 diagnoses readiness for it.

---

## Scope
**In scope:**
- 25-question self-assessment (5 per dimension x 5 dimensions), scored 1-5,
  CMMI-DMM aligned level anchors (Ad Hoc / Defined / Optimising)
- References: CMMI Data Management Maturity, DAMA DMBOK v2, Gartner Data
  Management Maturity Model, NHS Data Strategy (2021)
- Plotly radar chart: organisation score vs sector benchmark
- ReportLab PDF gap analysis report with prioritised recommendations
- Deploy to Streamlit Community Cloud

**Out of scope:**
- Any training dataset or ML model (this is a rules-based scoring tool)
- LLM/API integration (no .env keys required)
- Multi-tenant or persistent user accounts (single-session assessment only)

---

## Planned Architecture
See CLAUDE.md for the full folder structure and build order.

---

## Session Log

### Session 1 (2026-08-07): Question bank + scoring
- Designed 25 questions across 5 dimensions with CMMI-DMM level_1/level_3/
  level_5 anchor text (`assessment/questions.json`)
- Wrote `data/recommendations.json`: 3 recommended actions per dimension
- Wrote `data/benchmarks.csv`: NHS / Financial Services / Retail / SME
  sector benchmarks per dimension
- Built `assessment/scoring.py`: dimension scoring, overall score, RAG
  banding, benchmark lookup, gap ranking with attached recommendations
- Unit tested against 3 mock personas (low-maturity SME, mid-maturity NHS
  trust, high-maturity finance group) in `test-scenarios/`, all assertions
  passed: 25 questions across 5 dimensions confirmed, scoring correct at
  both ends of the scale
- Added project to VS Code workspace

### Reference library (2026-10-02): closed citation gaps
- Verified CMMI DMM PDF and NHS Data Strategy against their title/edition
  pages (Session 1 work), logged in `library/references.json`
- Caught that the DAMA-DMBOK file in the library was the First Edition
  (2009), not the Second Edition the brief cites. Replaced with the
  correct DMBOK2 (849 pages, contents page confirms Second Edition
  structure). Source is a third-party aggregator mirror (PDFDrive), not
  DAMA International or Technics Publications directly, noted in the
  manifest.
- Caught that the Gartner Data Management Maturity Model citation in
  scope had never actually been sourced. Located and verified
  "Gartner's Enterprise Information Management Maturity Model" (Douglas
  Laney, ID G00289832, 2016/2017), the closest genuine Gartner artifact
  to the brief's generic citation. Copy is watermarked to another named
  individual's paid Gartner seat, so it is licensed research, not public
  domain: kept out of the git repo (`library/*.pdf` gitignored), used
  only as private background reading, never to be published or embedded
  in any deliverable.
- All four reference documents (NHS, CMMI DMM, DAMA-DMBOK2, Gartner EIM)
  now logged in `library/references.json` with verification notes.

### Session 2 (2026-10-02): Streamlit dashboard
- Built `dashboard/app.py`: intro page, organisation name and sector
  inputs in the sidebar, session_state initialisation
- Built `dashboard/common.py`: shared session_state helpers, sidebar
  renderer, and cached data loaders, imported by every page so answers
  and sector selection persist across page navigation
- Built `dashboard/pages/01_assessment.py`: all 25 questions across 5
  dimensions, each with an expander showing the 1/3/5 CMMI level anchor
  text, slider scoring, progress bar
- Built `dashboard/pages/02_results.py`: overall score and RAG-flagged
  dimension scores, Plotly radar chart (org vs sector benchmark), top 5
  gaps with attached recommended actions
- Built `assessment/charts.py`: shared radar chart builder so the
  dashboard and the Session 3 PDF report use the identical chart
- Discovered `requirements.txt` had never actually been installed in the
  project venv (only pandas was present). Installed streamlit, plotly,
  reportlab, kaleido.
- Verified with Streamlit's `AppTest` harness (headless, no browser
  needed): all three pages run with zero exceptions in empty, partial,
  and fully-answered states; all 25 sliders render and set correctly;
  completing the assessment triggers the expected success message;
  scoring, benchmark lookup, and gap ranking all produce correct output
  end to end

### Session 3 (2026-10-03): PDF report
- Built `assessment/report_generator.py`: ReportLab PDF, embeds the same
  radar chart as the dashboard (via `charts.py` and kaleido), RAG-coloured
  scores table, top 5 gaps each with a dimension-specific cause and
  implication paragraph (drawn from each dimension's level_1/level_5
  anchor contrast in `questions.json`) plus its recommended actions
- Switched `assessment/charts.py` and the report's accent colour from
  teal to navy (`#14213D`) to match P9's established look, since P9 and
  P10 are presented as a pair; the dashboard radar and PDF radar share
  the same `build_radar_chart()` so they stay visually identical
- Built `dashboard/pages/03_report.py`: download button wired to
  `generate_report()`, gated on all 25 questions being answered
- Verified with `AppTest` (empty and fully-answered states, zero
  exceptions) and by generating an actual PDF and reading it back with
  pypdf: correct page count, scores table, gap text, and recommended
  actions all present and accurate against known mock-persona input

### Decision (2026-10-02/03): P9 and P10 stay separate apps
Discussed combining this tool with P9's self-assessment into one app or
one combined report ("v2.0" idea). Decided against a full merge: the two
scoring engines do not overlap (5 CMMI dimensions vs 8 NIST/EU AI Act
dimensions), P9 is already live at a bookmarked URL, and a real
consulting engagement diagnoses data foundations before raising AI
governance, so a combined assessment upfront would misrepresent the
actual sales motion. Decided to add a simple cross-link between the two
live apps now (not yet built) and treat a shared "combined scorecard"
report as a separate, later-scoped v2 feature. Both tools must be
positioned as a supporting pair, not a bundled product, in the eventual
LinkedIn launch post. Full reasoning saved to memory
(`project_p9_p10_pairing`).

### Session 4 (2026-10-08): Cross-link with P9
- Built the cross-link: `dashboard/common.py` now has `build_p9_link()`
  (maps P10 sector names onto P9's, builds a query-string URL) and
  `init_session_state()` reads incoming `org`/`sector` query params so a
  link from P9 can pre-fill P10 too. Added the link to the Results page,
  framed differently by RAG band: a red overall score tells the user to
  fix the data foundation first, amber/green frames the governance tool
  as the next question.
- Edited P9's `dashboard/app.py` to read the same `org`/`sector` query
  params on load (it had neither persisted to session state before).
  Verified locally with `AppTest`: no query params behaves identically to
  before this change, valid params pre-fill correctly, an unmapped
  sector (P10's SME / General has no P9 equivalent) falls back safely
  instead of crashing.
- Held P9's redeploy deliberately. The edit is verified locally but not
  pushed or redeployed, P9's live app still runs the pre-cross-link code.
  Decision: deploy P9's cross-link change and P10's first public release
  together, not separately, so the two tools go live as a pair rather
  than P9 changing underneath anyone before P10 exists to link to it.

## Next Actions
- Deploy P10 to Streamlit Community Cloud
- Write README, create GitHub repo, commit
- Push and redeploy P9's cross-link change at the same time P10 goes
  live (held back deliberately, see Session 4 above)
- Scope the "combined scorecard" report as a separate v2 feature once
  both tools are live
