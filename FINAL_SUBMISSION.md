# Final Submission — Week 12 Capstone
## Fintech Review Analytics for Ethiopian Banks

**Author:** Dagmawi  
**GitHub:** https://github.com/Dagi0808/fintech-review-analytics  
**Date:** July 2026

---

## Deliverables Checklist

| Deliverable | Status | Location |
|-------------|--------|----------|
| GitHub repository with all code | ✅ | https://github.com/Dagi0808/fintech-review-analytics |
| Refactored codebase (type hints, dataclasses, modular) | ✅ | `src/` |
| Unit and integration tests (61 passing) | ✅ | `tests/` |
| GitHub Actions CI/CD pipeline | ✅ | `.github/workflows/ci.yml` |
| Interactive Streamlit dashboard | ✅ | `dashboard/app.py` |
| SHAP model explainability | ✅ | `src/explainability.py` |
| Technical report | ✅ | `reports/technical_report.md` |
| Blog post | ✅ | `reports/blog_post.md` |
| Presentation script (10 slides) | ✅ | `reports/presentation_script.md` |
| Comprehensive README with CI badge | ✅ | `README.md` |
| Clean requirements.txt | ✅ | `requirements.txt` |
| Pipeline entry point | ✅ | `src/main.py` |

---

## Quick Start

```bash
git clone https://github.com/Dagi0808/fintech-review-analytics.git
cd fintech-review-analytics
pip install -r requirements.txt

# Run the dashboard (works with demo data immediately)
streamlit run dashboard/app.py

# Run the full pipeline (requires scraped data)
python -m src.main
```

---

## Project Structure

```
fintech-review-analytics/
├── .github/workflows/ci.yml       ← GitHub Actions CI/CD
├── dashboard/app.py               ← Streamlit interactive dashboard
├── data/raw/                      ← Scraped reviews (gitignored)
├── data/processed/                ← Pipeline outputs (gitignored)
├── reports/
│   ├── technical_report.md        ← Full technical report
│   ├── blog_post.md               ← Blog post / written report
│   ├── presentation_script.md     ← 10-slide presentation guide
│   └── interim_submission_1.md    ← First interim submission
├── src/
│   ├── config.py                  ← Dataclass configuration
│   ├── main.py                    ← Pipeline entry point (CLI)
│   ├── preprocessing.py           ← Data cleaning & validation
│   ├── sentiment_analysis.py      ← DistilBERT sentiment pipeline
│   ├── theme_extraction.py        ← Keyword theme classifier
│   ├── db_insert.py               ← PostgreSQL insertion
│   ├── explainability.py          ← SHAP explainability
│   └── utils.py                   ← Shared helper functions
├── tests/                         ← 61 pytest tests (all passing)
├── sql/schema.sql                 ← PostgreSQL schema
├── scripts/scrape_reviews.py      ← Google Play scraper
├── requirements.txt               ← Pinned dependencies
└── README.md                      ← Project documentation
```

---

## Key Results

| Bank | Avg Rating | % Positive | Top Complaint |
|------|-----------|------------|---------------|
| DASHEN | ~3.7 / 5 | ~68% | UI & UX Issues |
| BOA | ~3.2 / 5 | ~54% | Transaction Performance |
| CBE | ~2.8 / 5 | ~41% | Account Access Issues |

**Business recommendation:** CBE should prioritise fixing login and authentication failures — these drive the majority of negative reviews.

---

## Engineering Highlights

- **61 pytest tests** — all passing in under 3 seconds
- **GitHub Actions CI/CD** — runs lint + tests + coverage on every push
- **Zero hardcoded credentials** — all DB config via environment variables
- **Full type hints** on every function across all modules
- **@dataclass configuration** — all settings in `src/config.py`
- **Lazy ML imports** — tests run without GPU or model downloads
- **Demo mode dashboard** — works without running the pipeline

---

## CI Badge

[![CI Pipeline](https://github.com/Dagi0808/fintech-review-analytics/actions/workflows/ci.yml/badge.svg)](https://github.com/Dagi0808/fintech-review-analytics/actions/workflows/ci.yml)
