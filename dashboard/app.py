"""
Streamlit dashboard for the Fintech Review Analytics project.
Provides interactive exploration of customer sentiment and themes
for Ethiopian banks: CBE, BOA, and DASHEN.

Run with:
    streamlit run dashboard/app.py
"""
import os
from pathlib import Path
from typing import List

import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# ── Path resolution ────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "processed" / "reviews_with_themes.csv"

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Fintech Review Analytics",
    page_icon="🏦",
    layout="wide",
)

# ── Constants ─────────────────────────────────────────────────────────────────
BANKS: List[str] = ["CBE", "BOA", "DASHEN"]
BANK_COLORS: dict = {
    "CBE": "#1f77b4",
    "BOA": "#ff7f0e",
    "DASHEN": "#2ca02c",
}
SENTIMENT_COLORS: dict = {
    "POSITIVE": "#2ecc71",
    "NEGATIVE": "#e74c3c",
}


@st.cache_data
def load_data() -> pd.DataFrame:
    """Load the processed reviews with sentiment and themes.

    Returns:
        DataFrame, or a demo DataFrame if the data file is not found.
    """
    if DATA_PATH.exists():
        return pd.read_csv(DATA_PATH)

    # Demo data so the dashboard works without running the pipeline
    import numpy as np

    rng = np.random.default_rng(42)
    banks = rng.choice(BANKS, size=300)
    sentiments = rng.choice(
        ["POSITIVE", "NEGATIVE"],
        size=300,
        p=[0.6, 0.4],
    )
    themes = rng.choice(
        [
            "Account Access Issues",
            "Transaction Performance",
            "App Stability Issues",
            "OTP & Security Issues",
            "UI & UX Issues",
            "Feature Requests",
            "Other",
        ],
        size=300,
    )
    ratings = rng.integers(1, 6, size=300)
    dates = pd.date_range("2023-01-01", periods=300, freq="D")

    return pd.DataFrame(
        {
            "bank": banks,
            "review": [f"Sample review {i}" for i in range(300)],
            "sentiment_label": sentiments,
            "sentiment_score": rng.uniform(0.6, 1.0, size=300).round(3),
            "identified_theme": themes,
            "rating": ratings,
            "date": dates,
            "source": "google_play",
        }
    )


def sidebar_filters(df: pd.DataFrame):
    """Render sidebar filters and return filtered DataFrame.

    Args:
        df: Full review DataFrame.

    Returns:
        Filtered DataFrame based on sidebar selections.
    """
    st.sidebar.header("🔍 Filters")

    selected_banks = st.sidebar.multiselect(
        "Select Banks",
        options=BANKS,
        default=BANKS,
    )

    selected_sentiments = st.sidebar.multiselect(
        "Sentiment",
        options=["POSITIVE", "NEGATIVE"],
        default=["POSITIVE", "NEGATIVE"],
    )

    min_rating, max_rating = st.sidebar.slider(
        "Rating Range",
        min_value=1,
        max_value=5,
        value=(1, 5),
    )

    filtered = df[
        df["bank"].isin(selected_banks)
        & df["sentiment_label"].isin(selected_sentiments)
        & df["rating"].between(min_rating, max_rating)
    ]

    st.sidebar.metric("Filtered Reviews", f"{len(filtered):,}")
    return filtered


def render_overview(df: pd.DataFrame) -> None:
    """Render the overview KPI cards.

    Args:
        df: Filtered DataFrame.
    """
    col1, col2, col3, col4 = st.columns(4)
    total = len(df)
    pct_positive = round((df["sentiment_label"] == "POSITIVE").mean() * 100, 1)
    avg_rating = round(df["rating"].mean(), 2)
    top_complaint = (
        df[df["sentiment_label"] == "NEGATIVE"]["identified_theme"]
        .value_counts()
        .idxmax()
        if len(df[df["sentiment_label"] == "NEGATIVE"]) > 0
        else "N/A"
    )

    col1.metric("Total Reviews", f"{total:,}")
    col2.metric("% Positive", f"{pct_positive}%")
    col3.metric("Avg Rating", f"{avg_rating} / 5")
    col4.metric("Top Complaint", top_complaint)


def render_sentiment_charts(df: pd.DataFrame) -> None:
    """Render sentiment distribution charts.

    Args:
        df: Filtered DataFrame.
    """
    st.subheader("📊 Sentiment Distribution")
    col1, col2 = st.columns(2)

    # Pie chart — overall
    with col1:
        sentiment_counts = df["sentiment_label"].value_counts().reset_index()
        sentiment_counts.columns = ["Sentiment", "Count"]
        fig = px.pie(
            sentiment_counts,
            names="Sentiment",
            values="Count",
            color="Sentiment",
            color_discrete_map=SENTIMENT_COLORS,
            title="Overall Sentiment Split",
        )
        st.plotly_chart(fig, use_container_width=True)

    # Bar chart — by bank
    with col2:
        bank_sentiment = (
            df.groupby(["bank", "sentiment_label"])
            .size()
            .reset_index(name="count")
        )
        fig = px.bar(
            bank_sentiment,
            x="bank",
            y="count",
            color="sentiment_label",
            barmode="group",
            color_discrete_map=SENTIMENT_COLORS,
            title="Sentiment by Bank",
            labels={"count": "Number of Reviews", "bank": "Bank"},
        )
        st.plotly_chart(fig, use_container_width=True)


def render_rating_analysis(df: pd.DataFrame) -> None:
    """Render average rating and rating distribution charts.

    Args:
        df: Filtered DataFrame.
    """
    st.subheader("⭐ Rating Analysis")
    col1, col2 = st.columns(2)

    with col1:
        avg_ratings = df.groupby("bank")["rating"].mean().round(2).reset_index()
        fig = px.bar(
            avg_ratings,
            x="bank",
            y="rating",
            color="bank",
            color_discrete_map=BANK_COLORS,
            title="Average Rating by Bank",
            labels={"rating": "Average Rating", "bank": "Bank"},
            range_y=[0, 5],
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = px.histogram(
            df,
            x="rating",
            color="bank",
            barmode="overlay",
            color_discrete_map=BANK_COLORS,
            title="Rating Distribution by Bank",
            labels={"rating": "Star Rating", "count": "Count"},
            nbins=5,
        )
        st.plotly_chart(fig, use_container_width=True)


def render_theme_analysis(df: pd.DataFrame) -> None:
    """Render customer complaint theme analysis.

    Args:
        df: Filtered DataFrame.
    """
    st.subheader("🏷️ Customer Complaint Themes")
    col1, col2 = st.columns(2)

    with col1:
        theme_counts = df["identified_theme"].value_counts().reset_index()
        theme_counts.columns = ["Theme", "Count"]
        fig = px.bar(
            theme_counts,
            x="Count",
            y="Theme",
            orientation="h",
            title="All Themes (Frequency)",
            labels={"Count": "Number of Reviews"},
            color="Count",
            color_continuous_scale="Blues",
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Negative reviews only
        neg_df = df[df["sentiment_label"] == "NEGATIVE"]
        if len(neg_df) > 0:
            neg_theme_bank = (
                neg_df.groupby(["bank", "identified_theme"])
                .size()
                .reset_index(name="count")
            )
            fig = px.bar(
                neg_theme_bank,
                x="identified_theme",
                y="count",
                color="bank",
                barmode="stack",
                color_discrete_map=BANK_COLORS,
                title="Negative Reviews by Theme & Bank",
                labels={"count": "Count", "identified_theme": "Theme"},
            )
            fig.update_xaxes(tickangle=30)
            st.plotly_chart(fig, use_container_width=True)


def render_business_insights(df: pd.DataFrame) -> None:
    """Render actionable business recommendations based on data.

    Args:
        df: Filtered DataFrame.
    """
    st.subheader("💡 Business Insights")

    neg_df = df[df["sentiment_label"] == "NEGATIVE"]
    for bank in df["bank"].unique():
        bank_neg = neg_df[neg_df["bank"] == bank]
        if len(bank_neg) == 0:
            continue
        top_issue = bank_neg["identified_theme"].value_counts().idxmax()
        pct = round(len(bank_neg) / len(df[df["bank"] == bank]) * 100, 1)
        avg_r = round(df[df["bank"] == bank]["rating"].mean(), 2)

        with st.expander(f"🏦 {bank} — Avg Rating: {avg_r} | {pct}% Negative"):
            st.markdown(f"**Top Complaint:** {top_issue}")
            top_theme_counts = bank_neg["identified_theme"].value_counts().head(3)
            for theme, count in top_theme_counts.items():
                st.write(f"- {theme}: {count} reviews")
            st.info(
                f"💬 **Recommendation for {bank}:** Focus engineering resources "
                f"on resolving '{top_issue}' to improve customer satisfaction."
            )


def render_raw_reviews(df: pd.DataFrame) -> None:
    """Render a searchable table of raw reviews.

    Args:
        df: Filtered DataFrame.
    """
    st.subheader("📝 Review Explorer")
    col1, col2 = st.columns(2)
    bank_filter = col1.selectbox("Bank", ["All"] + BANKS)
    sentiment_filter = col2.selectbox("Sentiment", ["All", "POSITIVE", "NEGATIVE"])

    view = df.copy()
    if bank_filter != "All":
        view = view[view["bank"] == bank_filter]
    if sentiment_filter != "All":
        view = view[view["sentiment_label"] == sentiment_filter]

    st.dataframe(
        view[["bank", "review", "rating", "sentiment_label", "sentiment_score", "identified_theme"]]
        .sort_values("sentiment_score", ascending=False)
        .head(100),
        use_container_width=True,
    )


# ── Main layout ────────────────────────────────────────────────────────────────

def main() -> None:
    """Entry point for the Streamlit dashboard."""
    st.title("🏦 Fintech Review Analytics Dashboard")
    st.markdown(
        "Analyzing **1,502 customer reviews** from Ethiopian banks: "
        "**CBE**, **BOA**, and **DASHEN** — transforming raw feedback into business intelligence."
    )

    df = load_data()

    if len(df) == 0:
        st.warning("No data loaded. Run the pipeline first or check data/processed/.")
        return

    # Show demo badge if using synthetic data
    if not DATA_PATH.exists():
        st.warning("⚠️ Using demo data — run the pipeline to load real reviews.")

    filtered_df = sidebar_filters(df)

    if len(filtered_df) == 0:
        st.warning("No reviews match your current filters.")
        return

    # Tabs for navigation
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["📈 Overview", "😊 Sentiment", "⭐ Ratings", "🏷️ Themes", "📝 Reviews"]
    )

    with tab1:
        render_overview(filtered_df)
        render_business_insights(filtered_df)

    with tab2:
        render_sentiment_charts(filtered_df)

    with tab3:
        render_rating_analysis(filtered_df)

    with tab4:
        render_theme_analysis(filtered_df)

    with tab5:
        render_raw_reviews(filtered_df)

    # Footer
    st.markdown("---")
    st.caption("Built with Streamlit · Data from Google Play · Ethiopian Fintech Review Analytics")


if __name__ == "__main__":
    main()
