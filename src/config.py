"""
Configuration for the Fintech Review Analytics pipeline.
Uses dataclasses for clean, typed configuration objects.
"""
from dataclasses import dataclass, field
from typing import List


# ── Named constants ────────────────────────────────────────────────────────────
SENTIMENT_MODEL: str = "distilbert-base-uncased-finetuned-sst-2-english"
SENTIMENT_THRESHOLD: float = 0.7
TFIDF_MAX_FEATURES: int = 50
TFIDF_NGRAM_RANGE: tuple = (1, 2)

BANK_ID_MAP: dict = {
    "CBE": 1,
    "BOA": 2,
    "DASHEN": 3,
}

BANKS: List[str] = list(BANK_ID_MAP.keys())

THEME_KEYWORDS: dict = {
    "Account Access Issues": ["login", "password", "sign in"],
    "OTP & Security Issues": ["otp", "code", "verification"],
    "Transaction Performance": ["slow", "delay", "transfer", "payment"],
    "App Stability Issues": ["crash", "bug", "error"],
    "UI & UX Issues": ["ui", "design", "interface", "navigation"],
    "Feature Requests": ["feature", "fingerprint", "update"],
}


@dataclass
class PathConfig:
    """File path configuration for the pipeline."""

    raw_reviews: str = "data/raw/reviews_raw.csv"
    processed_reviews: str = "data/processed/reviews_clean.csv"
    sentiment_output: str = "data/processed/reviews_with_sentiment.csv"
    themes_output: str = "data/processed/reviews_with_themes.csv"


@dataclass
class DatabaseConfig:
    """PostgreSQL database connection configuration."""

    host: str = "localhost"
    port: int = 5432
    dbname: str = "bank_reviews"
    user: str = "postgres"
    password: str = ""

    @property
    def url(self) -> str:
        """Build SQLAlchemy connection URL."""
        return (
            f"postgresql://{self.user}:{self.password}"
            f"@{self.host}:{self.port}/{self.dbname}"
        )


@dataclass
class SentimentConfig:
    """Configuration for the sentiment analysis step."""

    model_name: str = SENTIMENT_MODEL
    threshold: float = SENTIMENT_THRESHOLD
    batch_size: int = 32
    truncation: bool = True
    max_length: int = 512


@dataclass
class PipelineConfig:
    """Top-level configuration that composes all sub-configs."""

    paths: PathConfig = field(default_factory=PathConfig)
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    sentiment: SentimentConfig = field(default_factory=SentimentConfig)
