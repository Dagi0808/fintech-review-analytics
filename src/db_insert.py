"""
Database insertion module for the Fintech Review Analytics pipeline.
Loads processed reviews into PostgreSQL via SQLAlchemy.
"""
import os
from typing import List

import pandas as pd
from sqlalchemy import create_engine, Engine

from src.config import DatabaseConfig, PathConfig, BANK_ID_MAP

# Columns expected in the final CSV before DB insertion
REVIEW_COLUMNS: List[str] = [
    "bank_id",
    "review_text",
    "rating",
    "review_date",
    "sentiment_label",
    "sentiment_score",
    "identified_theme",
    "source",
]


def build_engine(config: DatabaseConfig | None = None) -> Engine:
    """Create a SQLAlchemy engine from the database config.

    Args:
        config: DatabaseConfig instance; reads from env vars when omitted.

    Returns:
        SQLAlchemy Engine.
    """
    cfg = config or _config_from_env()
    return create_engine(cfg.url)


def _config_from_env() -> DatabaseConfig:
    """Build DatabaseConfig from environment variables with safe defaults.

    Returns:
        DatabaseConfig populated from environment variables.
    """
    return DatabaseConfig(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5432")),
        dbname=os.getenv("DB_NAME", "bank_reviews"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", ""),
    )


def load_data(path: str) -> pd.DataFrame:
    """Load the fully processed reviews CSV.

    Args:
        path: Path to the CSV file.

    Returns:
        DataFrame ready for database insertion.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Data file not found: {path}")
    return pd.read_csv(path)


def prepare_reviews(df: pd.DataFrame) -> pd.DataFrame:
    """Map bank names to IDs and select DB columns.

    Args:
        df: Raw processed DataFrame with a 'bank' column.

    Returns:
        DataFrame with exactly the columns required for the 'reviews' table.
    """
    df = df.copy()
    df["bank_id"] = df["bank"].map(BANK_ID_MAP)

    # Rename 'review' → 'review_text' if needed
    if "review" in df.columns and "review_text" not in df.columns:
        df = df.rename(columns={"review": "review_text"})
    if "date" in df.columns and "review_date" not in df.columns:
        df = df.rename(columns={"date": "review_date"})

    return df[REVIEW_COLUMNS]


def insert_reviews(
    df: pd.DataFrame,
    engine: Engine,
    if_exists: str = "append",
) -> int:
    """Insert a prepared reviews DataFrame into the database.

    Args:
        df: DataFrame with the correct columns (see REVIEW_COLUMNS).
        engine: SQLAlchemy Engine.
        if_exists: 'append' or 'replace'.

    Returns:
        Number of rows inserted.
    """
    df.to_sql("reviews", engine, if_exists=if_exists, index=False)
    return len(df)


def main() -> None:
    """Load processed reviews and insert them into PostgreSQL."""
    paths = PathConfig()
    engine = build_engine()

    raw_df = load_data(paths.themes_output)
    reviews_df = prepare_reviews(raw_df)

    count = insert_reviews(reviews_df, engine)
    print(f"✅ {count:,} reviews inserted into the database.")


if __name__ == "__main__":
    main()
