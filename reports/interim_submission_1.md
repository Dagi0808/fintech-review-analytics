# First Interim Submission
## Fintech Review Analytics — Week 12 Capstone

**Submitted by:** Dagmawi  
**Date:** July 22, 2026  
**GitHub:** https://github.com/Dagi0808/fintech-review-analytics

---

## 1. Selected Project

**Project Name:** Fintech Review Analytics for Ethiopian Banks

**Repository:** https://github.com/Dagi0808/fintech-review-analytics

**Why this project?**  
This project directly targets the finance sector — it analyses real customer reviews from Ethiopia's three largest commercial banks (CBE, BOA, and DASHEN) scraped from Google Play. It combines NLP, data engineering, and business analytics, making it the strongest candidate for a finance-sector portfolio piece. It already has a working pipeline and real data, so the week can be spent entirely on engineering quality, not rebuilding from scratch.

---

## 2. Business Problem Summary

Ethiopian banks receive thousands of customer reviews on Google Play every month. Reading and categorising them manually is impossible at scale. Product managers, operations teams, and customer experience leads have no systematic way to know:

- Which bank has the most dissatisfied customers?
- What specific issues are driving negative sentiment?
- Is the situation improving or getting worse over time?

This project solves that by automating the full pipeline from raw reviews to actionable business insights — classifying sentiment, identifying complaint themes, and surfacing recommendations through an interactive dashboard.

**Business value:** A bank that can identify "login failures are causing 40% of negative reviews for CBE" can direct engineering resources precisely, instead of guessing.

---

## 3. What Was Accomplished in the Original Project

The original project (completed in Week 2) included:

| Component | Status |
|-----------|--------|
| Google Play scraper (CBE, BOA, DASHEN) | ✅ Complete |
| Raw data collection — 1,502 reviews | ✅ Complete |
| PostgreSQL database schema + insertion | ✅ Complete |
| DistilBERT sentiment analysis pipeline | ✅ Complete |
| Keyword-based theme extraction | ✅ Complete |
| Basic EDA in Jupyter notebooks | ✅ Complete |
| README documentation | ⚠️ Partial |
| Unit tests | ❌ Missing |
| CI/CD pipeline | ❌ Missing |
| Interactive dashboard | ❌ Missing |
| Type hints and modular code structure | ⚠️ Partial |
| SHAP explainability | ❌ Missing |
| config.py / dataclass configuration | ❌ Missing |

---

## 4. Gap Analysis

| Category | Question | Status |
|----------|----------|--------|
| Code Quality | Is the code modular and well-organised? | Partial |
| Code Quality | Are there type hints on functions? | No |
| Code Quality | Is there a clear project structure? | Partial |
| Testing | Are there unit tests for core functions? | No |
| Testing | Do tests run automatically on push? | No |
| Documentation | Is the README comprehensive? | Partial |
| Documentation | Are there docstrings on functions? | Partial |
| Reproducibility | Can someone else run this project? | Partial |
| Reproducibility | Are dependencies in requirements.txt? | Yes (but bloated) |
| Visualization | Is there an interactive way to explore results? | No |
| Business Impact | Is the problem clearly articulated? | Partial |
| Business Impact | Are success metrics defined? | No |

---

## 5. Improvement Priorities (3–5 High-Impact Items)

| Priority | Improvement | Time Estimate | Impact |
|----------|-------------|---------------|--------|
| 1 | **Code refactoring** — modular `src/` structure, type hints, `@dataclass` config, docstrings on all functions | 4 hours | High — foundation for everything else |
| 2 | **pytest test suite** — minimum 5 tests covering preprocessing, sentiment, theme extraction, utils | 3 hours | High — proves reliability to finance employers |
| 3 | **GitHub Actions CI/CD** — auto-run tests + linting on every push, CI badge in README | 2 hours | High — demonstrates professional engineering practice |
| 4 | **Streamlit dashboard** — interactive exploration of sentiment, ratings, themes, business insights | 6 hours | High — most visible deliverable for non-technical stakeholders |
| 5 | **SHAP explainability** — global feature importance + local review explanation | 3 hours | Medium — shows ML transparency, valued in finance |

**Total estimated effort:** ~18 hours over 4 days

---

## 6. Day-by-Day Plan

### Day 1 — Wednesday 22 July (Today)
**Focus: Code Refactoring + Foundation**

- [x] Restructure project: `src/`, `tests/`, `dashboard/`, `data/`, `scripts/`
- [x] Create `src/config.py` with `@dataclass` configuration objects and named constants
- [x] Add `src/preprocessing.py` — typed preprocessing pipeline
- [x] Refactor `src/sentiment_analysis.py` — type hints, batch processing, docstrings
- [x] Refactor `src/theme_extraction.py` — type hints, NaN handling, docstrings
- [x] Refactor `src/db_insert.py` — functions, env-var DB config, no hardcoded credentials
- [x] Add `src/utils.py` — shared helpers (clean_text, validate_dataframe, filter_banks, etc.)
- [x] Add `src/main.py` — single CLI entry point for the full pipeline
- [x] Clean `requirements.txt` — remove GPU/CUDA bloat, pin essential packages

**Deliverable:** Fully refactored, modular codebase pushed to GitHub

---

### Day 2 — Thursday 23 July
**Focus: Testing + CI/CD**

- [x] Write `tests/test_preprocessing.py` — 17 tests
- [x] Write `tests/test_theme_extraction.py` — 20 tests
- [x] Write `tests/test_utils.py` — 18 tests
- [x] Write `tests/test_sentiment_analysis.py` — 6 tests
- [x] Write `tests/test_output.py` — integration tests with skip guards
- [x] Configure `.github/workflows/ci.yml` — lint + pytest + coverage gate
- [x] Add CI badge to README
- [x] All 61 tests passing locally

**Deliverable:** Green CI pipeline, 61 passing tests

---

### Day 3 — Friday 24 July
**Focus: Streamlit Dashboard**

- [x] Build `dashboard/app.py` — 5 interactive tabs
  - Overview: KPI cards (total reviews, % positive, avg rating, top complaint)
  - Sentiment: pie chart + bank comparison bar chart
  - Ratings: average rating + distribution histogram
  - Themes: complaint frequency + theme-by-bank breakdown
  - Reviews: searchable, filterable review table
- [x] Add sidebar filters (bank, sentiment, rating range)
- [x] Add business insight expanders with recommendations per bank
- [x] Demo mode with synthetic data (works without running pipeline)
- [ ] Capture screenshots for README / submission

**Deliverable:** Working Streamlit dashboard (`streamlit run dashboard/app.py`)

---

### Day 4 — Saturday–Sunday 26 July
**Focus: Explainability + Documentation + Report**

- [x] Add `src/explainability.py` — SHAP global importance + local text explanation
- [ ] Run SHAP on sample negative reviews, capture screenshots
- [ ] Update README with dashboard screenshots and SHAP plots
- [ ] Write technical blog post / report (PDF)
- [ ] Build 10-slide presentation deck
- [ ] Final review of all code quality
- [ ] Push final commit + tag `v1.0.0`

**Deliverable:** Complete portfolio project ready for final submission

---

## 7. Current Progress (as of Day 1/2)

**Already completed ahead of schedule:**

✅ Full code refactoring (Day 1 goal — done)  
✅ 61 pytest tests passing (Day 2 goal — done)  
✅ GitHub Actions CI/CD pipeline live  
✅ Streamlit dashboard built with 5 tabs  
✅ SHAP explainability module added  
✅ `src/main.py` pipeline entry point  
✅ Clean `requirements.txt`  
✅ All code pushed to GitHub  

**Remaining (Days 3–4):**  
- [ ] Run dashboard with real data + capture screenshots  
- [ ] Run SHAP on real reviews + save plots  
- [ ] Technical report / blog post  
- [ ] Presentation slides (10 slides)  
- [ ] README screenshots section

---

## 8. GitHub Evidence

All work is committed and pushed. Key commits:

1. `feat: production-grade refactor for finance portfolio` — refactored codebase, 44 tests, CI/CD, dashboard
2. `feat: add preprocessing, explainability, SHAP module and full test suite` — 17 more tests, SHAP module

**Link:** https://github.com/Dagi0808/fintech-review-analytics
