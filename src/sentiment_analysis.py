"""
Sentiment analysis module for Ethiopian bank reviews.
Uses a DistilBERT model to classify each review as POSITIVE or NEGATIVE.
"""
import os
from typing import List, Dict, Any

import pandas as pd

from src.config import PathConfig, SentimentConfig, SENTIMENT_THRESHOLD

# Lazy import — avoids requiring transformers/torch at test-time
try:
    from transformers import pipeline, Pipeline  # type: ignore
except ImportError:  # pragma: no cover
    pipeline = None  # type: ignore
    Pipeline = object  # type: ignore


def load_data(path: str) -> pd.DataFrame:
    """Load a cleaned review CSV from disk.

    Args:
        path: Relative or absolute path to the CSV file.

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


def init_model(config: SentimentConfig | None = None) -> Pipeline:
    """Initialise the Hugging Face sentiment pipeline.

    Args:
        config: Optional SentimentConfig; uses defaults when omitted.

    Returns:
        A HuggingFace text-classification pipeline.
    """
    cfg = config or SentimentConfig()
    model = pipeline(
        "sentiment-analysis",
        model=cfg.model_name,
        truncation=cfg.truncation,
        max_length=cfg.max_length,
    )
    print(f"Model loaded: {cfg.model_name}")
    return model


def run_sentiment(
    df: pd.DataFrame,
    model: Pipeline,
    batch_size: int = 32,
) -> pd.DataFrame:
    """Run batch sentiment prediction over the review column.

    Args:
        df: DataFrame containing a 'review' column.
        model: Initialised HuggingFace pipeline.
        batch_size: Number of reviews per batch.

    Returns:
        DataFrame with 'sentiment_label' and 'sentiment_score' columns added.
    """
    reviews: List[str] = df["review"].astype(str).tolist()
    results: List[Dict[str, Any]] = []

    for i in range(0, len(reviews), batch_size):
        batch = reviews[i : i + batch_size]
        results.extend(model(batch))

    df = df.copy()
    df["sentiment_label"] = [r["label"] for r in results]
    df["sentiment_score"] = [round(r["score"], 4) for r in results]
    return df


def filter_by_confidence(
    df: pd.DataFrame,
    threshold: float = SENTIMENT_THRESHOLD,
) -> pd.DataFrame:
    """Keep only reviews whose sentiment confidence meets the threshold.

    Args:
        df: DataFrame with a 'sentiment_score' column.
        threshold: Minimum confidence score to retain.

    Returns:
        Filtered DataFrame.
    """
    filtered = df[df["sentiment_score"] >= threshold].copy()
    removed = len(df) - len(filtered)
    print(f"Filtered {removed} low-confidence predictions (threshold={threshold})")
    return filtered


def print_summary(df: pd.DataFrame) -> None:
    """Print a basic sentiment distribution summary to stdout.

    Args:
        df: DataFrame with 'bank', 'sentiment_label', and 'sentiment_score' columns.
    """
    print("\n📊 Sentiment Distribution by Bank")
    print(df.groupby("bank")["sentiment_label"].value_counts().to_string())
    print("\n📊 Average Confidence Score by Bank")
    print(df.groupby("bank")["sentiment_score"].mean().round(4).to_string())


def save_output(df: pd.DataFrame, output_path: str) -> None:
    """Save the enriched DataFrame to CSV.

    Args:
        df: DataFrame to save.
        output_path: Destination file path.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"\n✅ Saved {len(df):,} rows to {output_path}")


def main() -> None:
    """End-to-end sentiment analysis pipeline entry point."""
    paths = PathConfig()
    sentiment_cfg = SentimentConfig()

    df = load_data(paths.processed_reviews)
    model = init_model(sentiment_cfg)
    df = run_sentiment(df, model, batch_size=sentiment_cfg.batch_size)
    print_summary(df)
    save_output(df, paths.sentiment_output)


if __name__ == "__main__":
    main()
