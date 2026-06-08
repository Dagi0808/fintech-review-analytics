# Scripts
# 📥 Google Play Review Scraping

## Purpose
This script collects user reviews from Google Play Store for Ethiopian banking apps.

## Banks Covered
- Commercial Bank of Ethiopia (CBE)
- Bank of Abyssinia (BOA)
- Dashen Bank

## Data Collected
- Review text
- Rating (1–5)
- Date
- Bank name
- Source (Google Play)

## Tool Used
- google-play-scraper

## Output
Saved as:
- data/raw/reviews_raw.csv

## Run
```bash
python scripts/scrape_reviews.py