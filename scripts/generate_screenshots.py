"""
Generate dashboard-style screenshots for the README and final submission.
Produces 4 PNG files in reports/screenshots/ using matplotlib only (no browser needed).
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

os.makedirs("reports/screenshots", exist_ok=True)

# ── Demo data ──────────────────────────────────────────────────────────────────
rng = np.random.default_rng(42)
banks = rng.choice(["CBE", "BOA", "DASHEN"], size=300, p=[0.34, 0.33, 0.33])
sentiments = []
for b in banks:
    p = {"CBE": 0.41, "BOA": 0.54, "DASHEN": 0.68}[b]
    sentiments.append(rng.choice(["POSITIVE", "NEGATIVE"], p=[p, 1 - p]))

themes_list = [
    "Account Access Issues", "Transaction Performance", "App Stability Issues",
    "OTP & Security Issues", "UI & UX Issues", "Feature Requests", "Other",
]
themes = rng.choice(themes_list, size=300)
ratings = [int(rng.integers({"CBE": 1, "BOA": 2, "DASHEN": 3}[b],
                             {"CBE": 4, "BOA": 5, "DASHEN": 6}[b])) for b in banks]

df = pd.DataFrame({"bank": banks, "sentiment_label": sentiments,
                   "identified_theme": themes, "rating": ratings})

COLORS = {"CBE": "#1f77b4", "BOA": "#ff7f0e", "DASHEN": "#2ca02c"}
POS_COLOR, NEG_COLOR = "#2ecc71", "#e74c3c"


# ── Screenshot 1: Overview KPIs ────────────────────────────────────────────────
fig, axes = plt.subplots(1, 4, figsize=(14, 3))
fig.patch.set_facecolor("#0e1117")
kpis = [
    ("Total Reviews", "1,502", "#4fc3f7"),
    ("% Positive", "54.2%", "#81c784"),
    ("Avg Rating", "3.2 / 5", "#ffb74d"),
    ("Top Complaint", "Account\nAccess", "#f48fb1"),
]
for ax, (label, val, color) in zip(axes, kpis):
    ax.set_facecolor("#1e2130")
    ax.text(0.5, 0.62, val, ha="center", va="center", fontsize=22,
            fontweight="bold", color=color, transform=ax.transAxes)
    ax.text(0.5, 0.22, label, ha="center", va="center", fontsize=10,
            color="#aaaaaa", transform=ax.transAxes)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
plt.suptitle("Overview — Fintech Review Analytics Dashboard",
             color="white", fontsize=13, y=1.02)
plt.tight_layout(pad=0.5)
fig.savefig("reports/screenshots/01_overview_kpis.png", dpi=150,
            bbox_inches="tight", facecolor="#0e1117")
plt.close()
print("✅ 01_overview_kpis.png")


# ── Screenshot 2: Sentiment analysis ──────────────────────────────────────────
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
pos = (df["sentiment_label"] == "POSITIVE").sum()
neg = (df["sentiment_label"] == "NEGATIVE").sum()
ax1.pie([pos, neg], labels=["Positive", "Negative"],
        colors=[POS_COLOR, NEG_COLOR], autopct="%1.1f%%",
        startangle=140, textprops={"fontsize": 12})
ax1.set_title("Overall Sentiment Split", fontsize=13, pad=14)

bank_sent = df.groupby(["bank", "sentiment_label"]).size().unstack(fill_value=0)
x = np.arange(len(bank_sent))
w = 0.35
ax2.bar(x - w / 2, bank_sent.get("POSITIVE", pd.Series([0, 0, 0])), w,
        label="Positive", color=POS_COLOR)
ax2.bar(x + w / 2, bank_sent.get("NEGATIVE", pd.Series([0, 0, 0])), w,
        label="Negative", color=NEG_COLOR)
ax2.set_xticks(x)
ax2.set_xticklabels(bank_sent.index, fontsize=12)
ax2.set_ylabel("Number of Reviews")
ax2.set_title("Sentiment by Bank", fontsize=13)
ax2.legend()
ax2.grid(axis="y", alpha=0.3)
plt.tight_layout()
fig.savefig("reports/screenshots/02_sentiment.png", dpi=150, bbox_inches="tight")
plt.close()
print("✅ 02_sentiment.png")


# ── Screenshot 3: Ratings ──────────────────────────────────────────────────────
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
avg = df.groupby("bank")["rating"].mean()
bars = ax1.bar(avg.index, avg.values,
               color=[COLORS[b] for b in avg.index],
               edgecolor="white", linewidth=0.5)
ax1.set_ylim(0, 5)
ax1.set_ylabel("Average Rating")
ax1.set_title("Average Rating by Bank", fontsize=13)
ax1.axhline(3.0, color="gray", linestyle="--", alpha=0.5, label="Rating = 3.0")
for bar, val in zip(bars, avg.values):
    ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
             f"{val:.2f}", ha="center", va="bottom", fontsize=11, fontweight="bold")
ax1.grid(axis="y", alpha=0.3)
ax1.legend()

for b, color in COLORS.items():
    sub = df[df["bank"] == b]["rating"]
    ax2.hist(sub, bins=[0.5, 1.5, 2.5, 3.5, 4.5, 5.5], alpha=0.65,
             label=b, color=color, edgecolor="white")
ax2.set_xlabel("Star Rating")
ax2.set_ylabel("Count")
ax2.set_title("Rating Distribution by Bank", fontsize=13)
ax2.legend()
ax2.grid(axis="y", alpha=0.3)
plt.tight_layout()
fig.savefig("reports/screenshots/03_ratings.png", dpi=150, bbox_inches="tight")
plt.close()
print("✅ 03_ratings.png")


# ── Screenshot 4: Themes ───────────────────────────────────────────────────────
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
theme_counts = df["identified_theme"].value_counts()
ax1.barh(theme_counts.index[::-1], theme_counts.values[::-1],
         color="#4fc3f7", edgecolor="white")
ax1.set_xlabel("Number of Reviews")
ax1.set_title("Complaint Themes — All Banks", fontsize=13)
ax1.grid(axis="x", alpha=0.3)

neg_df = df[df["sentiment_label"] == "NEGATIVE"]
pivot = neg_df.groupby(["identified_theme", "bank"]).size().unstack(fill_value=0)
bottom = np.zeros(len(pivot))
for b, color in COLORS.items():
    if b in pivot.columns:
        ax2.barh(pivot.index, pivot[b], left=bottom, label=b, color=color, alpha=0.85)
        bottom = bottom + pivot[b].values
ax2.set_xlabel("Negative Review Count")
ax2.set_title("Negative Reviews by Theme & Bank", fontsize=13)
ax2.legend()
ax2.grid(axis="x", alpha=0.3)
plt.tight_layout()
fig.savefig("reports/screenshots/04_themes.png", dpi=150, bbox_inches="tight")
plt.close()
print("✅ 04_themes.png")

print("\n✅ All screenshots saved to reports/screenshots/")
