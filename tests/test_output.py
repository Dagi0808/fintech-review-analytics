"""
Integration-style tests for pipeline output validation.
Verifies that processed CSV files have the expected structure.
"""
import pytest
import pandas as pd
from pathlib import Path

from src.utils import validate_dataframe
from src.config import PathConfig

# ── Helpers ────────────────────────────────────────────────────────────────────

PATHS = PathConfig()
REQUIRED_RAW_COLS = ["review", "rating", "date", "bank", "source"]
REQUIRED_PROCESSED_COLS = [
    "review",
    "rating",
    "date",
    "bank",
    "source",
    "sentiment_label",
    "sentiment_score",
    "identified_theme",
]


def _load_if_exists(path: str) -> pd.DataFrame | None:
    """Return a DataFrame if the file exists, else None."""
    p = Path(path)
    if not p.exists():
        return None
    return pd.read_csv(p)


# ── Raw data tests (skipped when data not yet scraped) ─────────────────────────

class TestRawData:
    @pytest.fixture
    def raw_df(self):
        df = _load_if_exists(PATHS.raw_reviews)
        if df is None:
            pytest.skip("Raw data not available — run scripts/scrape_reviews.py first")
        return df

    def test_has_required_columns(self, raw_df):
        validate_dataframe(raw_df, REQUIRED_RAW_COLS)

    def test_no_empty_reviews(self, raw_df):
        assert raw_df["review"].notna().all(), "Found null reviews in raw data"

    def test_rating_range(self, raw_df):
        assert raw_df["rating"].between(1, 5).all(), "Ratings must be 1–5"

    def test_banks_are_valid(self, raw_df):
        valid_banks = {"CBE", "BOA", "DASHEN"}
        assert set(raw_df["bank"].unique()).issubset(valid_banks)

    def test_minimum_review_count(self, raw_df):
        assert len(raw_df) >= 400, f"Expected ≥400 reviews, got {len(raw_df)}"


# ── Processed data tests (skipped when pipeline not yet run) ───────────────────

class TestProcessedData:
    @pytest.fixture
    def processed_df(self):
        df = _load_if_exists(PATHS.themes_output)
        if df is None:
            pytest.skip("Processed data not available — run the pipeline first")
        return df

    def test_has_sentiment_columns(self, processed_df):
        validate_dataframe(processed_df, ["sentiment_label", "sentiment_score"])

    def test_has_theme_column(self, processed_df):
        validate_dataframe(processed_df, ["identified_theme"])

    def test_sentiment_labels_are_valid(self, processed_df):
        valid = {"POSITIVE", "NEGATIVE"}
        assert set(processed_df["sentiment_label"].unique()).issubset(valid)

    def test_sentiment_score_range(self, processed_df):
        assert processed_df["sentiment_score"].between(0.0, 1.0).all()

    def test_no_null_themes(self, processed_df):
        assert processed_df["identified_theme"].notna().all()

    def test_all_three_banks_present(self, processed_df):
        banks = set(processed_df["bank"].unique())
        assert "CBE" in banks and "BOA" in banks and "DASHEN" in banks
