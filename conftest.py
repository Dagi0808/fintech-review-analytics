"""
pytest configuration — ensures the project root is on sys.path
so that `from src.xxx import ...` works without installation.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
