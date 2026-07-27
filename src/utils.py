"""
Shared utility functions for the Fintech Review Analytics pipeline.
"""
import re
from typing import List, Optional

import pandas as pd


def clean_review_text(text: str) -> str:
    """Normalise a single review string for NLP processing.

    Converts to lowercase, strips punctuation, and collapses whitespace.

    Args:
        text: Raw review string.

    Returns:
        Cleaned, lowercase string.
    """
    text = str(text).lower()
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def validate_dataframe(df: pd.DataFrame, required_columns: List[str]) -> None:
    """Assert that a DataFrame contains all required columns.

    Args:
        df: DataFrame to validate.
        required_columns: List of column names that must be present.

    Raises:
        ValueError: If any required column is missing.
    """
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")


def sentiment_label_to_int(label: str) -> int:
    """Convert a sentiment label string to a numeric representation.

    Args:
        label: 'POSITIVE' or 'NEGATIVE'.

    Returns:
        1 for positive, 0 for negative, -1 for unknown.
    """
    mapping = {"POSITIVE": 1, "NEGATIVE": 0}
    return mapping.get(label.upper(), -1)


def filter_banks(df: pd.DataFrame, banks: Optional[List[str]] = None) -> pd.DataFrame:
    """Filter a DataFrame to only rows matching the given banks.

    Args:
        df: DataFrame with a 'bank' column.
        banks: List of bank names to keep. If None, returns df unchanged.

    Returns:
        Filtered DataFrame.
    """
    if banks is None:
        return df
    return df[df["bank"].isin(banks)].copy()


def compute_sentiment_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Compute per-bank sentiment statistics.

    Args:
        df: DataFrame with 'bank', 'sentiment_label', 'sentiment_score', 'rating'.

    Returns:
        DataFrame with one row per bank and summary statistics.
    """
    stats = (
        df.groupby("bank")
        .agg(
            total_reviews=("review", "count"),
            avg_rating=("rating", "mean"),
            avg_confidence=("sentiment_score", "mean"),
            pct_positive=(
                "sentiment_label",
                lambda x: round((x == "POSITIVE").mean() * 100, 1),
            ),
        )
        .reset_index()
    )
    return stats
