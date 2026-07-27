"""
Preprocessing module for the Fintech Review Analytics pipeline.
Cleans and validates raw scraped reviews before sentiment analysis.
"""
import os
from typing import List

import pandas as pd

from src.config import PathConfig

# Columns that must exist in the raw CSV
REQUIRED_COLUMNS: List[str] = ["review", "rating", "date", "bank", "source"]

# Valid bank names
VALID_BANKS: List[str] = ["CBE", "BOA", "DASHEN"]


def load_raw(path: str) -> pd.DataFrame:
    """Load the raw scraped reviews CSV.

    Args:
        path: Path to the raw CSV file.

    Returns:
        Raw DataFrame.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If required columns are missing.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Raw data not found: {path}")

    df = pd.read_csv(path)
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns in raw data: {missing}")

    print(f"Loaded {len(df):,} raw reviews from {path}")
    return df


def drop_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicate reviews (same text and bank).

    Args:
        df: Raw DataFrame.

    Returns:
        Deduplicated DataFrame.
    """
    original_len = len(df)
    df = df.drop_duplicates(subset=["review", "bank"]).copy()
    removed = original_len - len(df)
    if removed:
        print(f"Removed {removed:,} duplicate reviews")
    return df


def drop_nulls(df: pd.DataFrame) -> pd.DataFrame:
    """Drop rows where the review text is null or empty.

    Args:
        df: DataFrame with a 'review' column.

    Returns:
        DataFrame with null/empty reviews removed.
    """
    original_len = len(df)
    df = df[df["review"].notna() & (df["review"].astype(str).str.strip() != "")].copy()
    removed = original_len - len(df)
    if removed:
        print(f"Removed {removed:,} null/empty reviews")
    return df


def validate_ratings(df: pd.DataFrame) -> pd.DataFrame:
    """Keep only rows with valid ratings (1–5).

    Args:
        df: DataFrame with a 'rating' column.

    Returns:
        DataFrame with invalid ratings removed.
    """
    original_len = len(df)
    df = df[df["rating"].between(1, 5)].copy()
    removed = original_len - len(df)
    if removed:
        print(f"Removed {removed:,} rows with invalid ratings")
    return df


def normalise_bank_names(df: pd.DataFrame) -> pd.DataFrame:
    """Standardise bank name casing and filter to known banks.

    Args:
        df: DataFrame with a 'bank' column.

    Returns:
        DataFrame with uppercase, validated bank names.
    """
    df = df.copy()
    df["bank"] = df["bank"].astype(str).str.upper().str.strip()
    unknown = df[~df["bank"].isin(VALID_BANKS)]["bank"].unique()
    if len(unknown) > 0:
        print(f"Warning: Unknown bank names found and removed: {list(unknown)}")
        df = df[df["bank"].isin(VALID_BANKS)]
    return df


def add_review_length(df: pd.DataFrame) -> pd.DataFrame:
    """Add a 'review_length' column (word count) for feature engineering.

    Args:
        df: DataFrame with a 'review' column.

    Returns:
        DataFrame with 'review_length' column added.
    """
    df = df.copy()
    df["review_length"] = df["review"].astype(str).str.split().str.len()
    return df


def run_preprocessing(df: pd.DataFrame) -> pd.DataFrame:
    """Execute the full preprocessing pipeline.

    Args:
        df: Raw scraped DataFrame.

    Returns:
        Cleaned, validated DataFrame ready for sentiment analysis.
    """
    df = drop_duplicates(df)
    df = drop_nulls(df)
    df = validate_ratings(df)
    df = normalise_bank_names(df)
    df = add_review_length(df)

    print(f"\n✅ Preprocessing complete: {len(df):,} reviews remain")
    return df


def save_clean(df: pd.DataFrame, output_path: str) -> None:
    """Save the cleaned DataFrame to CSV.

    Args:
        df: Cleaned DataFrame.
        output_path: Destination file path.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"✅ Saved cleaned data to {output_path}")


def main() -> None:
    """End-to-end preprocessing pipeline entry point."""
    paths = PathConfig()
    df = load_raw(paths.raw_reviews)
    clean_df = run_preprocessing(df)
    save_clean(clean_df, paths.processed_reviews)


if __name__ == "__main__":
    main()
