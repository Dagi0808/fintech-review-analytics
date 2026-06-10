import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import os


def load_data(path):
    df = pd.read_csv(path)
    print(f"Loaded data: {df.shape}")
    return df


def clean_text(df):
    df["review"] = df["review"].astype(str).str.lower()
    df["review"] = df["review"].str.replace(r"[^a-zA-Z\s]", "", regex=True)
    return df


def extract_keywords(df):
    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        max_features=50
    )

    X = vectorizer.fit_transform(df["review"])
    keywords = vectorizer.get_feature_names_out()

    return keywords


def assign_theme(text):
    text = str(text).lower()

    if any(x in text for x in ["login", "password", "sign in"]):
        return "Account Access Issues"

    elif any(x in text for x in ["otp", "code", "verification"]):
        return "OTP & Security Issues"

    elif any(x in text for x in ["slow", "delay", "transfer", "payment"]):
        return "Transaction Performance"

    elif any(x in text for x in ["crash", "bug", "error"]):
        return "App Stability Issues"

    elif any(x in text for x in ["ui", "design", "interface", "navigation"]):
        return "UI & UX Issues"

    elif any(x in text for x in ["feature", "fingerprint", "update"]):
        return "Feature Requests"

    else:
        return "Other"


def analyze_themes(df):
    df["identified_theme"] = df["review"].apply(assign_theme)

    print("\n📊 Theme Distribution by Bank")
    print(df.groupby("bank")["identified_theme"].value_counts())

    return df


def save_output(df, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"\n✅ Saved: {output_path}")


def main():
    input_path = "data/processed/reviews_with_sentiment.csv"
    output_path = "data/processed/reviews_with_themes.csv"

    df = load_data(input_path)

    df = clean_text(df)

    keywords = extract_keywords(df)
    print("\n🔑 Top Keywords:")
    print(keywords[:20])

    df = analyze_themes(df)

    save_output(df, output_path)


if __name__ == "__main__":
    main()