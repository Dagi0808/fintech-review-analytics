"""
Model explainability module for the Fintech Review Analytics pipeline.
Uses SHAP to explain sentiment model predictions at both global and local levels.

Note: Requires 'shap' and 'transformers' to be installed.
Install with: pip install shap transformers torch
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import List, Optional

import numpy as np
import pandas as pd

try:
    import shap
    import matplotlib.pyplot as plt
    from transformers import pipeline as hf_pipeline
    _SHAP_AVAILABLE = True
except ImportError:  # pragma: no cover
    _SHAP_AVAILABLE = False


def _require_shap() -> None:
    """Raise ImportError with install instructions if shap is not available."""
    if not _SHAP_AVAILABLE:
        raise ImportError(
            "shap, transformers, and matplotlib are required for explainability.\n"
            "Install with: pip install shap transformers torch matplotlib"
        )


def build_text_explainer(
    model_name: str = "distilbert-base-uncased-finetuned-sst-2-english",
    num_samples: int = 100,
) -> "shap.Explainer":
    """Build a SHAP explainer for a HuggingFace text-classification pipeline.

    Args:
        model_name: HuggingFace model identifier.
        num_samples: Number of background samples for the masker.

    Returns:
        shap.Explainer instance wrapping the model pipeline.
    """
    _require_shap()
    clf = hf_pipeline(
        "text-classification",
        model=model_name,
        return_all_scores=True,
        truncation=True,
        max_length=512,
    )
    explainer = shap.Explainer(clf)
    return explainer


def explain_sample(
    explainer: "shap.Explainer",
    texts: List[str],
) -> "shap.Explanation":
    """Compute SHAP values for a list of review texts.

    Args:
        explainer: Pre-built SHAP explainer.
        texts: List of review strings to explain.

    Returns:
        shap.Explanation object with token-level SHAP values.
    """
    _require_shap()
    shap_values = explainer(texts)
    return shap_values


def plot_global_importance(
    df: pd.DataFrame,
    output_dir: str = "reports/figures",
    top_n: int = 20,
) -> None:
    """Plot global feature importance using TF-IDF token frequencies
    weighted by sentiment score as a proxy for model importance.

    This is a lightweight alternative to full SHAP global plots when
    running the pipeline without a GPU.

    Args:
        df: DataFrame with 'review', 'sentiment_label', 'sentiment_score' columns.
        output_dir: Directory to save the plot PNG.
        top_n: Number of top tokens to display.
    """
    _require_shap()
    from sklearn.feature_extraction.text import TfidfVectorizer

    os.makedirs(output_dir, exist_ok=True)

    neg_reviews = df[df["sentiment_label"] == "NEGATIVE"]["review"].astype(str).tolist()

    if len(neg_reviews) < 5:
        print("Not enough negative reviews for global importance plot.")
        return

    vectorizer = TfidfVectorizer(stop_words="english", max_features=200, ngram_range=(1, 2))
    X = vectorizer.fit_transform(neg_reviews)
    scores = np.asarray(X.mean(axis=0)).flatten()
    tokens = vectorizer.get_feature_names_out()

    top_idx = scores.argsort()[-top_n:][::-1]
    top_tokens = tokens[top_idx]
    top_scores = scores[top_idx]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(top_tokens[::-1], top_scores[::-1], color="#e74c3c")
    ax.set_xlabel("Mean TF-IDF Score (Negative Reviews)")
    ax.set_title(f"Top {top_n} Keywords in Negative Reviews\n(Proxy for Complaint Drivers)")
    ax.grid(axis="x", linestyle="--", alpha=0.4)
    plt.tight_layout()

    out_path = os.path.join(output_dir, "global_importance.png")
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    print(f"✅ Global importance plot saved to {out_path}")


def plot_local_explanation(
    explainer: "shap.Explainer",
    text: str,
    label: str = "NEGATIVE",
    output_dir: str = "reports/figures",
) -> None:
    """Generate and save a SHAP text plot for a single review.

    Args:
        explainer: Pre-built SHAP text explainer.
        text: Single review string to explain.
        label: Target label to highlight ('POSITIVE' or 'NEGATIVE').
        output_dir: Directory to save the HTML output.
    """
    _require_shap()
    os.makedirs(output_dir, exist_ok=True)

    shap_values = explainer([text])

    # Save as HTML (best format for token-level text explanations)
    out_path = os.path.join(output_dir, "local_explanation.html")
    html = shap.plots.text(shap_values[0], display=False)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ Local SHAP explanation saved to {out_path}")


def explain_bank_complaints(
    df: pd.DataFrame,
    bank: str,
    n_samples: int = 10,
    output_dir: str = "reports/figures",
    model_name: str = "distilbert-base-uncased-finetuned-sst-2-english",
) -> None:
    """Run full SHAP explainability for the most negative reviews of a given bank.

    Generates both a global importance proxy plot and a local explanation
    for the single most negative review.

    Args:
        df: Processed DataFrame with sentiment and theme columns.
        bank: Bank name to analyse ('CBE', 'BOA', or 'DASHEN').
        n_samples: Number of negative reviews to use for local explanations.
        output_dir: Directory to save all output figures.
        model_name: HuggingFace model to use for SHAP explanations.
    """
    _require_shap()

    bank_df = df[df["bank"] == bank].copy()
    neg_df = bank_df[bank_df["sentiment_label"] == "NEGATIVE"].sort_values(
        "sentiment_score", ascending=False
    )

    if len(neg_df) == 0:
        print(f"No negative reviews found for {bank}.")
        return

    bank_dir = os.path.join(output_dir, bank.lower())
    os.makedirs(bank_dir, exist_ok=True)

    # Global proxy plot
    plot_global_importance(bank_df, output_dir=bank_dir)

    # Local SHAP explanation for the top negative review
    top_negative = neg_df["review"].iloc[0]
    explainer = build_text_explainer(model_name=model_name)
    plot_local_explanation(explainer, top_negative, output_dir=bank_dir)

    print(f"\n✅ Explainability analysis complete for {bank}")
    print(f"   Top complaint: {neg_df['identified_theme'].value_counts().idxmax()}")
    print(f"   Most negative review: {top_negative[:120]}...")
