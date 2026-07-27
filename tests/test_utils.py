"""
Unit tests for src/utils.py
"""
import pytest
import pandas as pd

from src.utils import (
    clean_review_text,
    validate_dataframe,
    sentiment_label_to_int,
    filter_banks,
    compute_sentiment_stats,
)


class TestCleanReviewText:
    def test_lowercases(self):
        assert clean_review_text("HELLO") == "hello"

    def test_strips_punctuation(self):
        result = clean_review_text("Hello, World!")
        assert "," not in result
        assert "!" not in result

    def test_collapses_whitespace(self):
        result = clean_review_text("too   many    spaces")
        assert "  " not in result

    def test_empty_string(self):
        assert clean_review_text("") == ""

    def test_only_numbers_stripped(self):
        result = clean_review_text("Test 123")
        assert "1" not in result


class TestValidateDataframe:
    def _df(self):
        return pd.DataFrame({"bank": ["CBE"], "review": ["ok"], "rating": [4]})

    def test_passes_with_all_columns(self):
        validate_dataframe(self._df(), ["bank", "review", "rating"])

    def test_raises_on_missing_column(self):
        with pytest.raises(ValueError, match="Missing required columns"):
            validate_dataframe(self._df(), ["bank", "sentiment_label"])

    def test_empty_required_list_always_passes(self):
        validate_dataframe(self._df(), [])


class TestSentimentLabelToInt:
    def test_positive_returns_one(self):
        assert sentiment_label_to_int("POSITIVE") == 1

    def test_negative_returns_zero(self):
        assert sentiment_label_to_int("NEGATIVE") == 0

    def test_unknown_returns_minus_one(self):
        assert sentiment_label_to_int("NEUTRAL") == -1

    def test_case_insensitive(self):
        assert sentiment_label_to_int("positive") == 1


class TestFilterBanks:
    def _df(self):
        return pd.DataFrame(
            {
                "bank": ["CBE", "BOA", "DASHEN", "CBE"],
                "review": ["a", "b", "c", "d"],
            }
        )

    def test_filters_to_selected_banks(self):
        result = filter_banks(self._df(), ["CBE"])
        assert set(result["bank"].unique()) == {"CBE"}
        assert len(result) == 2

    def test_none_returns_all_rows(self):
        df = self._df()
        result = filter_banks(df, None)
        assert len(result) == len(df)

    def test_multiple_banks(self):
        result = filter_banks(self._df(), ["CBE", "BOA"])
        assert len(result) == 3


class TestComputeSentimentStats:
    def _df(self):
        return pd.DataFrame(
            {
                "bank": ["CBE", "CBE", "BOA"],
                "review": ["bad app", "great app", "ok app"],
                "rating": [2, 5, 3],
                "sentiment_label": ["NEGATIVE", "POSITIVE", "POSITIVE"],
                "sentiment_score": [0.95, 0.98, 0.88],
            }
        )

    def test_returns_one_row_per_bank(self):
        result = compute_sentiment_stats(self._df())
        assert set(result["bank"]) == {"CBE", "BOA"}

    def test_pct_positive_calculation(self):
        result = compute_sentiment_stats(self._df())
        cbe = result[result["bank"] == "CBE"].iloc[0]
        assert cbe["pct_positive"] == 50.0

    def test_avg_rating_is_correct(self):
        result = compute_sentiment_stats(self._df())
        cbe = result[result["bank"] == "CBE"].iloc[0]
        assert abs(cbe["avg_rating"] - 3.5) < 0.01
