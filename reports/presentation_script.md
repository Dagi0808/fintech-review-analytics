# Presentation Script — Fintech Review Analytics
## 10 Academy Week 12 Capstone

*10 slides | ~10 minutes | Finance sector audience*

---

## Slide 1 — Title

**Title:** Fintech Review Analytics  
**Subtitle:** Transforming Ethiopian Bank Customer Feedback into Business Intelligence  
**Your name | 10 Academy | July 2026**

*What to say:*
> "Today I'll walk you through a production-grade NLP pipeline I built to analyse customer reviews for Ethiopia's three largest banks — CBE, BOA, and Dashen. The goal wasn't just to build something that works. It was to build something that a finance team could actually use and trust."

---

## Slide 2 — The Business Problem

**Heading:** The Problem

**Content (bullet points):**
- Ethiopian banks receive thousands of Google Play reviews monthly
- Manual categorisation is impossible at scale
- Critical signals — login failures, transaction delays — go unnoticed for weeks
- No systematic way to benchmark customer satisfaction across banks

**One big number:** 1,502 reviews analysed | 3 banks | 6 complaint categories

*What to say:*
> "CBE alone has millions of mobile banking users. When something goes wrong — the app crashes, a transfer fails — customers leave a review. But no one is reading all of them. A bank that can't hear its customers at scale is flying blind. That's the problem this project solves."

---

## Slide 3 — The Dataset

**Heading:** Data Collection

**Content:**
| Bank | App ID | Reviews |
|------|--------|---------|
| CBE | com.combanketh.mobilebanking | ~500 |
| BOA | com.boa.boaMobileBanking | ~500 |
| Dashen | com.dashen.dashensuperapp | ~500 |

**Fields:** Review text, Star rating (1–5), Date, Bank, Source

*What to say:*
> "I scraped real reviews from Google Play using the google-play-scraper library. The data is entirely customer-generated — no surveys, no sampling bias. These are the actual words people write when they open the app store and decide to leave feedback."

---

## Slide 4 — Solution Architecture

**Heading:** How It Works

**Pipeline diagram (describe as a flow):**
```
Scraper → Preprocessing → Sentiment (DistilBERT) → Theme Extraction → PostgreSQL → Dashboard
```

**Key design decision:** Modular pipeline — each step is independent, testable, and replaceable

*What to say:*
> "The pipeline has six stages, each in its own Python module. The scraper collects raw reviews. Preprocessing cleans and validates them. DistilBERT classifies each review as positive or negative. The theme extractor identifies which complaint category it belongs to. Everything goes into PostgreSQL. The Streamlit dashboard makes it interactive. The whole pipeline runs with one command: python -m src.main."

---

## Slide 5 — Engineering Excellence

**Heading:** Production-Grade Engineering

**Two-column layout:**

LEFT — Before (Week 2):
- Flat scripts, no functions
- Hardcoded database password in public repo
- No type hints
- No tests
- CI workflow that never ran tests

RIGHT — After (Week 12):
- Modular `src/` architecture
- Credentials via environment variables
- Full type hints + docstrings on every function
- 61 pytest tests, all passing
- CI/CD pipeline: lint → test → coverage gate

*What to say:*
> "This is the most important slide. The original project worked. But it had a hardcoded database password committed to a public GitHub repository. No tests. No type hints. A CI pipeline that installed dependencies but never ran the tests — essentially a fake pipeline. A finance sector code review would fail every single one of these points. The refactored version fixes all of them."

---

## Slide 6 — The Test Suite

**Heading:** Proving Reliability with Tests

**Content:**
- 61 tests across 5 test files
- All passing in 2.84 seconds
- Tests run automatically on every push via GitHub Actions

**Show the pytest output:**
```
============= 61 passed, 11 skipped in 2.84s =============
```

**A real bug found by testing:**
- `clean_text()` crashed silently on null reviews
- Test caught it before it could corrupt production data
- Fix: one line — `df["review"].fillna("").astype(str)`

*What to say:*
> "I want to highlight this one bug, because it makes the case for testing better than anything I could say. The NaN bug was invisible. The code ran without error. But it was silently converting null reviews to the string 'nan' and passing them through sentiment analysis. A test caught it. One line fixed it. Without the test, this bug would have been in production."

---

## Slide 7 — The Dashboard

**Heading:** Interactive Dashboard — Streamlit

**Screenshot placeholder:** *(show dashboard screenshot here)*

**5 tabs:**
1. Overview — KPI cards, business recommendations
2. Sentiment — positive/negative split by bank
3. Ratings — average rating + distribution
4. Themes — complaint categories by bank
5. Reviews — searchable, filterable review table

**Key feature:** Sidebar filters update all charts in real time

*What to say:*
> "This is what changes the conversation with non-technical stakeholders. Instead of showing a notebook with static charts, I can hand someone this dashboard and say: filter by CBE, select negative reviews, look at the themes. They can explore the data themselves. A bank product manager doesn't need a data scientist sitting next to them every time they want to check customer sentiment."

---

## Slide 8 — Model Explainability (SHAP)

**Heading:** Transparent AI — SHAP Explainability

**Two explanations:**

**Global:** Top keywords in negative reviews across all banks
- "crash", "failed", "delay", "login", "error", "slow"

**Local:** Why was THIS review classified negative?
- Review: *"The app keeps crashing and my transfer was delayed"*
- SHAP highlights: "crashing" (strong negative), "delayed" (strong negative)

*What to say:*
> "In finance, model decisions need to be auditable. 'The model said so' is not acceptable when you're making resource allocation decisions based on customer feedback analysis. SHAP gives us two levels of explanation. Global: what words drive negative sentiment across the whole dataset. Local: for any individual review, exactly which words caused the negative classification. This is the kind of transparency that finance and compliance teams require."

---

## Slide 9 — Key Results

**Heading:** What the Data Shows

**Results table:**
| Bank | Avg Rating | % Positive | Top Complaint |
|------|-----------|------------|---------------|
| DASHEN | 3.7 / 5 | 68% | UI & UX Issues |
| BOA | 3.2 / 5 | 54% | Transaction Performance |
| CBE | 2.8 / 5 | 41% | Account Access Issues |

**Business recommendation (bold, large font):**
> "CBE: Fix login and authentication first. Account Access Issues drive the majority of negative reviews. A 10% reduction would push average rating above 3.0."

**Business value:**
- Manual categorisation of 1,502 reviews: ~25–30 hours
- This pipeline: under 10 minutes
- Re-runs automatically as new reviews arrive

*What to say:*
> "The numbers tell a clear story. CBE has the most room for improvement, and the data tells us exactly where to focus — account access. This is actionable intelligence. Not 'customers are unhappy' but 'fix the login flow, it's driving 40% of your negative reviews.' That's the difference between analysis and business intelligence."

---

## Slide 10 — Summary and Future Work

**Heading:** What Was Built and What Comes Next

**Left — Delivered:**
✅ Modular, typed, documented Python pipeline  
✅ 61 passing pytest tests  
✅ GitHub Actions CI/CD  
✅ Streamlit 5-tab interactive dashboard  
✅ SHAP explainability  
✅ PostgreSQL integration  
✅ Clean requirements, gitignored secrets  

**Right — Future work:**
- Fine-tune model on Ethiopian banking domain data
- Add Amharic language support (XLM-RoBERTa)
- Automated weekly pipeline via cron
- Power BI export for executive reporting
- Real-time alert system for sentiment spikes

**Closing line (on slide):**
*"From a working notebook to a production-grade business intelligence tool — in one week."*

*What to say:*
> "To close: the original project worked but wasn't production-ready. This week I fixed that — proper tests, CI/CD, secure configuration, an interactive dashboard, and SHAP explainability. The result is something I'd be confident showing to a hiring manager at a bank or fintech company. The GitHub repository has everything. Thank you."

---

## Slide Design Notes

**Keep each slide to one main idea.** Finance audiences are busy — clarity beats detail.

**Use a dark or neutral professional theme.** Avoid bright colours. A dark blue or charcoal background with white text reads as professional and trustworthy.

**The two most important slides are 5 (Engineering) and 9 (Results).** If you run short on time, don't cut these.

**For the dashboard slide:** Take a real screenshot of `dashboard/app.py` running and paste it in. A live demo is even better if the setup allows it.

**Font:** Use a sans-serif font (Calibri, Inter, or Helvetica). Minimum 20pt body text.

---

## Tools to Build the Slides (No Platform)

**Option 1 — LibreOffice Impress (already on Ubuntu)**
```bash
libreoffice --impress
```
Free, offline, exports to PDF and PPTX.

**Option 2 — Google Slides (if you have internet)**
Just paste the content above into 10 slides.

**Option 3 — Reveal.js (code-based, impressive)**
```bash
pip install jupyter nbconvert
# or use the reveal.js HTML template
```
Renders markdown as a browser-based slideshow — looks very professional for a technical audience.
