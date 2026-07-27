"""
Unit tests for src/theme_extraction.py
"""
import pytest
import pandas as pd

from src.theme_extraction import assign_theme, clean_text, analyze_themes, get_top_themes


# ── assign_theme ───────────────────────────────────────────────────────────────

class TestAssignTheme:
    def test_login_keyword_returns_account_access(self):
        assert assign_theme("I cannot login to the app") == "Account Access Issues"

    def test_password_keyword_returns_account_access(self):
        assert assign_theme("Forgot my password again") == "Account Access Issues"

    def test_otp_keyword_returns_security(self):
        assert assign_theme("OTP never arrives on time") == "OTP & Security Issues"

    def test_slow_keyword_returns_transaction(self):
        assert assign_theme("Transfer is very slow and delays payment") == "Transaction Performance"

    def test_crash_keyword_returns_stability(self):
        assert assign_theme("App keeps crashing with an error") == "App Stability Issues"

    def test_ui_keyword_returns_ux(self):
        assert assign_theme("The interface design is confusing") == "UI & UX Issues"

    def test_feature_keyword_returns_feature_request(self):
        assert assign_theme("Please add fingerprint feature update") == "Feature Requests"

    def test_unmatched_text_returns_other(self):
        assert assign_theme("Great bank overall") == "Other"

    def test_empty_string_returns_other(self):
        assert assign_theme("") == "Other"

    def test_case_insensitive(self):
        assert assign_theme("LOGIN FAILED") == "Account Access Issues"


# ── clean_text ─────────────────────────────────────────────────────────────────

class TestCleanText:
    def _make_df(self, reviews):
        return pd.DataFrame({"review": reviews, "bank": ["CBE"] * len(reviews)})

    def test_lowercases_text(self):
        df = self._make_df(["GREAT APP"])
        result = clean_text(df)
        assert result["review"].iloc[0] == "great app"

    def test_removes_punctuation(self):
        df = self._make_df(["Hello, world!"])
        result = clean_text(df)
        assert result["review"].iloc[0] == "hello world"

    def test_strips_numbers(self):
        df = self._make_df(["Top 5 banks 2024"])
        result = clean_text(df)
        assert "5" not in result["review"].iloc[0]
        assert "2024" not in result["review"].iloc[0]

    def test_preserves_raw_review(self):
        df = self._make_df(["Hello World!"])
        result = clean_text(df)
        assert result["review_raw"].iloc[0] == "Hello World!"

    def test_handles_nan(self):
        df = self._make_df([None])
        result = clean_text(df)
        # Should not raise; NaN becomes "nan" string
        assert isinstance(result["review"].iloc[0], str)


# ── analyze_themes ─────────────────────────────────────────────────────────────

class TestAnalyzeThemes:
    def _make_df(self):
        return pd.DataFrame(
            {
                "review": [
                    "login failed multiple times",
                    "transfer is always slow",
                    "great app love it",
                ],
                "bank": ["CBE", "BOA", "DASHEN"],
            }
        )

    def test_adds_identified_theme_column(self):
        df = self._make_df()
        result = analyze_themes(df)
        assert "identified_theme" in result.columns

    def test_correct_theme_count(self):
        df = self._make_df()
        result = analyze_themes(df)
        assert len(result) == 3

    def test_does_not_mutate_input(self):
        df = self._make_df()
        _ = analyze_themes(df)
        assert "identified_theme" not in df.columns


# ── get_top_themes ─────────────────────────────────────────────────────────────

class TestGetTopThemes:
    def test_returns_correct_number(self):
        df = pd.DataFrame(
            {"identified_theme": ["A", "A", "B", "B", "B", "C"]}
        )
        result = get_top_themes(df, n=2)
        assert len(result) == 2

    def test_returns_most_common_first(self):
        df = pd.DataFrame(
            {"identified_theme": ["A", "B", "B", "B", "C", "C"]}
        )
        result = get_top_themes(df, n=1)
        assert result.index[0] == "B"
