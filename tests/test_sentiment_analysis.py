"""
Unit tests for src/sentiment_analysis.py
(Tests that don't require a GPU or model download — pure logic tests)
"""
import pytest
import pandas as pd

from src.sentiment_analysis import filter_by_confidence, save_output
from src.config import SENTIMENT_THRESHOLD


class TestFilterByConfidence:
    def _df(self):
        return pd.DataFrame(
            {
                "review": ["good app", "bad app", "ok app"],
                "sentiment_label": ["POSITIVE", "NEGATIVE", "POSITIVE"],
                "sentiment_score": [0.98, 0.45, 0.72],
            }
        )

    def test_removes_low_confidence(self):
        result = filter_by_confidence(self._df(), threshold=0.7)
        assert len(result) == 2

    def test_keeps_all_above_threshold(self):
        result = filter_by_confidence(self._df(), threshold=0.4)
        assert len(result) == 3

    def test_default_threshold_used(self):
        df = self._df()
        result = filter_by_confidence(df)
        assert all(result["sentiment_score"] >= SENTIMENT_THRESHOLD)

    def test_does_not_mutate_input(self):
        df = self._df()
        original_len = len(df)
        _ = filter_by_confidence(df, threshold=0.9)
        assert len(df) == original_len


class TestSaveOutput:
    def test_creates_output_file(self, tmp_path):
        df = pd.DataFrame({"review": ["test"], "sentiment_label": ["POSITIVE"]})
        out_path = str(tmp_path / "output" / "results.csv")
        save_output(df, out_path)
        import os
        assert os.path.exists(out_path)

    def test_saved_file_has_correct_rows(self, tmp_path):
        df = pd.DataFrame({"review": ["a", "b", "c"]})
        out_path = str(tmp_path / "results.csv")
        save_output(df, out_path)
        loaded = pd.read_csv(out_path)
        assert len(loaded) == 3
