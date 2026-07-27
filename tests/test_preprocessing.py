"""
Unit tests for src/preprocessing.py
"""
import pytest
import pandas as pd

from src.preprocessing import (
    drop_duplicates,
    drop_nulls,
    validate_ratings,
    normalise_bank_names,
    add_review_length,
    run_preprocessing,
)


def _base_df(**overrides) -> pd.DataFrame:
    """Create a minimal valid raw DataFrame for testing."""
    data = {
        "review": ["App crashes often", "Great service", "Login failed", "Slow transfer"],
        "rating": [2, 5, 1, 3],
        "date": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04"],
        "bank": ["CBE", "DASHEN", "BOA", "CBE"],
        "source": ["Google Play"] * 4,
    }
    data.update(overrides)
    return pd.DataFrame(data)


class TestDropDuplicates:
    def test_removes_exact_duplicates(self):
        df = _base_df()
        df = pd.concat([df, df.iloc[:1]], ignore_index=True)  # add a duplicate
        result = drop_duplicates(df)
        assert len(result) == 4

    def test_keeps_same_review_different_bank(self):
        df = pd.DataFrame(
            {
                "review": ["good app", "good app"],
                "rating": [5, 4],
                "date": ["2024-01-01", "2024-01-02"],
                "bank": ["CBE", "BOA"],
                "source": ["Google Play", "Google Play"],
            }
        )
        result = drop_duplicates(df)
        assert len(result) == 2

    def test_does_not_mutate_input(self):
        df = _base_df()
        original_len = len(df)
        _ = drop_duplicates(df)
        assert len(df) == original_len


class TestDropNulls:
    def test_removes_null_reviews(self):
        df = _base_df()
        df.loc[0, "review"] = None
        result = drop_nulls(df)
        assert len(result) == 3

    def test_removes_empty_string_reviews(self):
        df = _base_df()
        df.loc[1, "review"] = "   "
        result = drop_nulls(df)
        assert len(result) == 3

    def test_keeps_valid_reviews(self):
        df = _base_df()
        result = drop_nulls(df)
        assert len(result) == 4


class TestValidateRatings:
    def test_removes_rating_above_five(self):
        df = _base_df()
        df.loc[0, "rating"] = 6
        result = validate_ratings(df)
        assert len(result) == 3

    def test_removes_rating_below_one(self):
        df = _base_df()
        df.loc[0, "rating"] = 0
        result = validate_ratings(df)
        assert len(result) == 3

    def test_keeps_boundary_ratings(self):
        df = pd.DataFrame(
            {
                "review": ["a", "b"],
                "rating": [1, 5],
                "date": ["2024-01-01", "2024-01-02"],
                "bank": ["CBE", "BOA"],
                "source": ["Google Play", "Google Play"],
            }
        )
        result = validate_ratings(df)
        assert len(result) == 2


class TestNormaliseBankNames:
    def test_uppercases_bank_names(self):
        df = _base_df()
        df.loc[0, "bank"] = "cbe"
        result = normalise_bank_names(df)
        assert result["bank"].iloc[0] == "CBE"

    def test_removes_unknown_banks(self):
        df = _base_df()
        df.loc[0, "bank"] = "UNKNOWN_BANK"
        result = normalise_bank_names(df)
        assert "UNKNOWN_BANK" not in result["bank"].values

    def test_strips_whitespace(self):
        df = _base_df()
        df.loc[0, "bank"] = "  CBE  "
        result = normalise_bank_names(df)
        assert result["bank"].iloc[0] == "CBE"


class TestAddReviewLength:
    def test_adds_review_length_column(self):
        df = _base_df()
        result = add_review_length(df)
        assert "review_length" in result.columns

    def test_length_is_word_count(self):
        df = pd.DataFrame(
            {
                "review": ["one two three"],
                "rating": [3],
                "date": ["2024-01-01"],
                "bank": ["CBE"],
                "source": ["Google Play"],
            }
        )
        result = add_review_length(df)
        assert result["review_length"].iloc[0] == 3


class TestRunPreprocessing:
    def test_returns_dataframe(self):
        df = _base_df()
        result = run_preprocessing(df)
        assert isinstance(result, pd.DataFrame)

    def test_adds_review_length(self):
        df = _base_df()
        result = run_preprocessing(df)
        assert "review_length" in result.columns

    def test_removes_invalid_data(self):
        df = _base_df()
        df = pd.concat(
            [df, pd.DataFrame([{"review": None, "rating": 9, "date": "x", "bank": "FAKE", "source": "x"}])],
            ignore_index=True,
        )
        result = run_preprocessing(df)
        assert len(result) <= len(df)
