import pandas as pd
from transformers import pipeline
import os


def load_data(path: str):
    """Load cleaned review dataset"""
    df = pd.read_csv(path)
    print(f"Loaded data: {df.shape}")
    return df


def init_model():
    """Initialize Hugging Face sentiment model"""
    model = pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english"
    )
    return model


def run_sentiment(df, model):
    """Run sentiment prediction on reviews"""
    results = []

    for review in df["review"]:
        result = model(str(review))[0]
        results.append(result)

    df["sentiment_label"] = [r["label"] for r in results]
    df["sentiment_score"] = [r["score"] for r in results]

    return df


def analyze(df):
    """Basic sentiment analytics"""
    print("\n📊 Sentiment Distribution by Bank")
    print(df.groupby("bank")["sentiment_label"].value_counts())

    print("\n📊 Average Confidence Score by Bank")
    print(df.groupby("bank")["sentiment_score"].mean())


def save_output(df, output_path: str):
    """Save enriched dataset"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"\n✅ Saved to {output_path}")


def main():
    input_path = "data/processed/reviews_clean.csv"
    output_path = "data/processed/reviews_with_sentiment.csv"

    df = load_data(input_path)

    model = init_model()

    df = run_sentiment(df, model)

    analyze(df)

    save_output(df, output_path)


if __name__ == "__main__":
    main()