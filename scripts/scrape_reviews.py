"""
Google Play review scraper for Ethiopian bank apps.
Scrapes reviews for CBE, BOA, and DASHEN and saves to data/raw/reviews_raw.csv.

Usage:
    python scripts/scrape_reviews.py
"""
import os
import time
from typing import Any, Dict, List

import pandas as pd
from google_play_scraper import Sort, reviews

# ── Configuration ──────────────────────────────────────────────────────────────

APPS: Dict[str, str] = {
    "CBE": "com.combanketh.mobilebanking",
    "BOA": "com.boa.boaMobileBanking",
    "DASHEN": "com.dashen.dashensuperapp",
}

TARGET_PER_BANK: int = 500       # Reviews to collect per bank
REQUEST_BATCH_SIZE: int = 200    # Reviews per API call
SLEEP_BETWEEN_REQUESTS: float = 1.0  # Seconds to wait between calls
OUTPUT_PATH: str = "data/raw/reviews_raw.csv"


# ── Scraper ────────────────────────────────────────────────────────────────────

def scrape_bank(app_name: str, app_id: str, target: int = TARGET_PER_BANK) -> List[Dict[str, Any]]:
    """Scrape reviews for a single bank app from Google Play.

    Args:
        app_name: Human-readable bank name (e.g. 'CBE').
        app_id: Google Play app ID.
        target: Number of reviews to collect.

    Returns:
        List of review dicts with keys: review, rating, date, bank, source.
    """
    print(f"\n🔄 Scraping {app_name} ({app_id}) ...")
    collected: List[Dict[str, Any]] = []
    continuation_token = None

    while len(collected) < target:
        result, continuation_token = reviews(
            app_id,
            lang="en",
            country="et",
            sort=Sort.NEWEST,
            count=REQUEST_BATCH_SIZE,
            continuation_token=continuation_token,
        )

        for r in result:
            collected.append(
                {
                    "review": r.get("content", ""),
                    "rating": r.get("score"),
                    "date": r.get("at").date() if r.get("at") else None,
                    "bank": app_name,
                    "source": "Google Play",
                }
            )

        print(f"  Collected {len(collected):,} reviews for {app_name}")

        if not continuation_token or len(result) == 0:
            break

        time.sleep(SLEEP_BETWEEN_REQUESTS)

    return collected[:target]


def scrape_all_banks(apps: Dict[str, str] = APPS) -> pd.DataFrame:
    """Scrape reviews for all configured banks.

    Args:
        apps: Mapping of bank name → Google Play app ID.

    Returns:
        Combined DataFrame of all scraped reviews.
    """
    all_reviews: List[Dict[str, Any]] = []

    for app_name, app_id in apps.items():
        bank_reviews = scrape_bank(app_name, app_id)
        all_reviews.extend(bank_reviews)
        print(f"  ✅ {app_name}: {len(bank_reviews):,} reviews")

    return pd.DataFrame(all_reviews)


def save_raw(df: pd.DataFrame, output_path: str = OUTPUT_PATH) -> None:
    """Save the raw scraped reviews to CSV.

    Args:
        df: DataFrame of scraped reviews.
        output_path: Destination CSV path.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"\n✅ Saved {len(df):,} reviews to {output_path}")


def main() -> None:
    """Entry point: scrape all banks and save raw data."""
    df = scrape_all_banks()
    save_raw(df)
    print(f"\nBank breakdown:")
    print(df.groupby("bank").size().to_string())


if __name__ == "__main__":
    main()
