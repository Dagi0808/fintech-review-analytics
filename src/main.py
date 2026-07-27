"""
Full pipeline entry point for the Fintech Review Analytics project.

Runs the complete sequence:
  1. Preprocess raw reviews
  2. Run sentiment analysis
  3. Extract themes
  4. Insert into PostgreSQL (optional)

Usage:
    python -m src.main                   # full pipeline (no DB insert)
    python -m src.main --with-db         # include DB insertion
    python -m src.main --step preprocess # single step
"""
import argparse
import sys
import time
from typing import Optional

import pandas as pd

from src.config import PathConfig, SentimentConfig, PipelineConfig
from src.preprocessing import load_raw, run_preprocessing, save_clean
from src.sentiment_analysis import load_data, init_model, run_sentiment, save_output
from src.theme_extraction import clean_text, analyze_themes, save_output as save_themes


# ── Step runners ───────────────────────────────────────────────────────────────

def step_preprocess(paths: PathConfig) -> None:
    """Run the preprocessing step.

    Args:
        paths: PathConfig with input/output paths.
    """
    print("\n" + "=" * 50)
    print("STEP 1 — PREPROCESSING")
    print("=" * 50)
    df = load_raw(paths.raw_reviews)
    clean_df = run_preprocessing(df)
    save_clean(clean_df, paths.processed_reviews)


def step_sentiment(paths: PathConfig, sentiment_cfg: SentimentConfig) -> None:
    """Run the sentiment analysis step.

    Args:
        paths: PathConfig with input/output paths.
        sentiment_cfg: SentimentConfig with model settings.
    """
    print("\n" + "=" * 50)
    print("STEP 2 — SENTIMENT ANALYSIS")
    print("=" * 50)
    df = load_data(paths.processed_reviews)
    model = init_model(sentiment_cfg)
    df = run_sentiment(df, model, batch_size=sentiment_cfg.batch_size)
    save_output(df, paths.sentiment_output)


def step_themes(paths: PathConfig) -> None:
    """Run the theme extraction step.

    Args:
        paths: PathConfig with input/output paths.
    """
    print("\n" + "=" * 50)
    print("STEP 3 — THEME EXTRACTION")
    print("=" * 50)
    df = load_data(paths.sentiment_output)
    df = clean_text(df)
    df = analyze_themes(df)
    save_themes(df, paths.themes_output)


def step_db_insert(paths: PathConfig) -> None:
    """Run the database insertion step.

    Args:
        paths: PathConfig with input/output paths.
    """
    print("\n" + "=" * 50)
    print("STEP 4 — DATABASE INSERT")
    print("=" * 50)
    # Import here to avoid requiring psycopg2 when not using DB
    from src.db_insert import build_engine, load_data as db_load, prepare_reviews, insert_reviews

    engine = build_engine()
    raw_df = db_load(paths.themes_output)
    reviews_df = prepare_reviews(raw_df)
    count = insert_reviews(reviews_df, engine)
    print(f"✅ Inserted {count:,} reviews into PostgreSQL")


# ── CLI ────────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        Namespace with parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Fintech Review Analytics Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m src.main                   Run full pipeline (skip DB)
  python -m src.main --with-db         Run full pipeline + DB insert
  python -m src.main --step preprocess Run only preprocessing
  python -m src.main --step sentiment  Run only sentiment analysis
  python -m src.main --step themes     Run only theme extraction
        """,
    )
    parser.add_argument(
        "--step",
        choices=["preprocess", "sentiment", "themes", "db"],
        default=None,
        help="Run a single pipeline step instead of the full pipeline",
    )
    parser.add_argument(
        "--with-db",
        action="store_true",
        default=False,
        help="Include database insertion step",
    )
    return parser.parse_args()


def run_full_pipeline(config: PipelineConfig, with_db: bool = False) -> None:
    """Execute all pipeline steps in sequence.

    Args:
        config: Top-level PipelineConfig.
        with_db: If True, also run the DB insertion step.
    """
    start = time.time()
    print("\n🚀 Starting Fintech Review Analytics Pipeline")
    print(f"   Banks: CBE | BOA | DASHEN")
    print(f"   Input: {config.paths.raw_reviews}")

    step_preprocess(config.paths)
    step_sentiment(config.paths, config.sentiment)
    step_themes(config.paths)

    if with_db:
        step_db_insert(config.paths)

    elapsed = round(time.time() - start, 1)
    print(f"\n✅ Pipeline complete in {elapsed}s")
    print(f"   Output: {config.paths.themes_output}")
    print(f"\nNext step: streamlit run dashboard/app.py")


def main() -> None:
    """CLI entry point."""
    args = parse_args()
    config = PipelineConfig()

    if args.step is None:
        run_full_pipeline(config, with_db=args.with_db)
    elif args.step == "preprocess":
        step_preprocess(config.paths)
    elif args.step == "sentiment":
        step_sentiment(config.paths, config.sentiment)
    elif args.step == "themes":
        step_themes(config.paths)
    elif args.step == "db":
        step_db_insert(config.paths)


if __name__ == "__main__":
    main()
