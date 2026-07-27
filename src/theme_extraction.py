"""
Theme extraction module for Ethiopian bank reviews.
Uses keyword matching + TF-IDF to classify customer complaints into themes.
"""
import os
import re
from typing import List

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

from src.config import PathConfig, THEME_KEYWORDS, TFIDF_MAX_FEATURES, TFIDF_NGRAM_RANGE


def load_data(path: str) -> pd.DataFrame:
    """Load a review CSV from disk.

    Args:
        path: Path to the CSV file.

    Returns:
        DataFrame with review data.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Data file not found: {path}")
    df = pd.read_csv(path)
    print(f"Loaded {len(df):,} reviews from {path}")
    return df


def clean_text(df: pd.DataFrame) -> pd.DataFrame:
    """Normalise the review column for NLP processing.

    Converts to lowercase and strips non-alphabetic characters.

    Args:
        df: DataFrame with a 'review' column.

    Returns:
        DataFrame with cleaned 'review' column (original preserved in 'review_raw').
    """
    df = df.copy()
    df["review_raw"] = df["review"]
    df["review"] = (
        df["review"]
        .fillna("")
        .astype(str)
        .str.lower()
        .pipe(lambda s: s.str.replace(r"[^a-zA-Z\s]", "", regex=True))
        .str.strip()
    )
    return df


def extract_keywords(df: pd.DataFrame) -> np.ndarray:
    """Extract top TF-IDF keywords from the review corpus.

    Args:
        df: DataFrame with a cleaned 'review' column.

    Returns:
        Array of top keyword strings.
    """
    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=TFIDF_NGRAM_RANGE,
        max_features=TFIDF_MAX_FEATURES,
    )
    vectorizer.fit_transform(df["review"])
    return vectorizer.get_feature_names_out()


def assign_theme(text: str) -> str:
    """Map a single review text to a complaint theme via keyword matching.

    Args:
        text: Raw or cleaned review string.

    Returns:
        Theme label string, or 'Other' if no keywords match.
    """
    text_lower = str(text).lower()
    for theme, keywords in THEME_KEYWORDS.items():
        if any(kw in text_lower for kw in keywords):
            return theme
    return "Other"


def analyze_themes(df: pd.DataFrame) -> pd.DataFrame:
    """Apply theme assignment to all reviews and print distribution.

    Args:
        df: DataFrame with a 'review' column.

    Returns:
        DataFrame with an 'identified_theme' column added.
    """
    df = df.copy()
    df["identified_theme"] = df["review"].apply(assign_theme)

    print("\n📊 Theme Distribution by Bank")
    print(df.groupby("bank")["identified_theme"].value_counts().to_string())
    return df


def get_top_themes(df: pd.DataFrame, n: int = 5) -> pd.Series:
    """Return the top N most common themes across all banks.

    Args:
        df: DataFrame with an 'identified_theme' column.
        n: Number of top themes to return.

    Returns:
        Series with theme counts, sorted descending.
    """
    return df["identified_theme"].value_counts().head(n)


def save_output(df: pd.DataFrame, output_path: str) -> None:
    """Save the themed DataFrame to CSV.

    Args:
        df: DataFrame to save.
        output_path: Destination file path.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"\n✅ Saved {len(df):,} rows to {output_path}")


def main() -> None:
    """End-to-end theme extraction pipeline entry point."""
    paths = PathConfig()

    df = load_data(paths.sentiment_output)
    df = clean_text(df)

    keywords = extract_keywords(df)
    print(f"\n🔑 Top {len(keywords)} TF-IDF Keywords:")
    print(", ".join(keywords[:20]))

    df = analyze_themes(df)

    print("\n🏷️ Top 5 Themes Overall:")
    print(get_top_themes(df).to_string())

    save_output(df, paths.themes_output)


if __name__ == "__main__":
    main()
