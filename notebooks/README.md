
# 📄 2. README — EDA Notebook

Create: `notebooks/README_eda.md`

```md id="eda_readme"
# 📊 Exploratory Data Analysis (EDA)

## Purpose
This notebook explores Google Play Store reviews to understand user feedback patterns.

## What is Analyzed
- Number of reviews per bank
- Rating distribution
- Basic review text inspection

## Dataset Used
- data/raw/reviews_raw.csv
- data/processed/reviews_clean.csv

## Key Insights (Initial)
- Banks have similar review volume
- Majority of reviews are either very positive or very negative
- Text data shows common complaints like login issues and slow transfers

## Run Notebook
```bash
jupyter notebook notebooks/eda.ipynb