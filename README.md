## 📊 Task 2 — Sentiment Analysis & Theme Extraction

This task focuses on analyzing Google Play Store reviews for Ethiopian banking apps (CBE, BOA, Dashen) using NLP techniques to extract sentiment and recurring user concerns.

---

### 🔧 Approach

The pipeline was implemented in two main stages:

#### 1. Sentiment Analysis
- Model: `distilbert-base-uncased-finetuned-sst-2-english`
- Tool: Hugging Face Transformers pipeline
- Output:
  - sentiment_label (POSITIVE / NEGATIVE)
  - sentiment_score (confidence score)

Each review was classified to measure user satisfaction across banks.

---

#### 2. Theme Extraction
- Method: TF-IDF (unigrams + bigrams)
- Library: Scikit-learn (TfidfVectorizer)
- Rule-based grouping of keywords into business themes:

Identified themes:
- Account Access Issues
- Transaction Performance
- OTP & Security Issues
- UI & UX Issues
- Feature Requests
- App Stability Issues
- Other

Each review was mapped to the most relevant theme based on keyword matching.

---

### 📊 Dataset Summary

- Initial scraped reviews: ~1,800
- After cleaning: 1,502 reviews
- Banks analyzed:
  - Commercial Bank of Ethiopia (CBE)
  - Bank of Abyssinia (BOA)
  - Dashen Bank

---

### 📈 Key Findings

- Dashen Bank has the highest proportion of positive reviews.
- BOA and CBE show higher negative sentiment.
- Transaction performance issues appear across all banks (systemic issue).
- A large portion of reviews fall under "Other", indicating limitations in rule-based classification.

---

### ⚠️ Limitations

- Rule-based theme classification may oversimplify complex reviews.
- "Other" category is large due to limited NLP modeling depth.
- Future improvement: topic modeling (LDA) or embedding-based clustering.

---

### 🚀 Next Steps

- Store processed data in PostgreSQL (Task 3)
- Improve theme extraction using advanced NLP models
- Build visualization dashboards for stakeholder reporting