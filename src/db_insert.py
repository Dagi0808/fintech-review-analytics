import pandas as pd
from sqlalchemy import create_engine
import os

engine = create_engine(
    "postgresql://postgres:selfmade@localhost:5432/bank_reviews"
)

df = pd.read_csv(
    os.path.join(os.path.dirname(__file__), "..", "data", "processed", "reviews_with_themes.csv")
)

bank_mapping = {
    "CBE": 1,
    "BOA": 2,
    "DASHEN": 3
}

df["bank_id"] = df["bank"].map(bank_mapping)

reviews_df = df[
    [
        "bank_id",
        "review",
        "rating",
        "date",
        "sentiment_label",
        "sentiment_score",
        "identified_theme",
        "source"
    ]
].copy()

reviews_df.columns = [
    "bank_id",
    "review_text",
    "rating",
    "review_date",
    "sentiment_label",
    "sentiment_score",
    "identified_theme",
    "source"
]
reviews_df.to_sql(
    "reviews",
    engine,
    if_exists="append",
    index=False
)

print(f"{len(reviews_df)} reviews inserted successfully.")