"""
Package setup for fintech-review-analytics.
Allows `pip install -e .` for development installs.
"""
from setuptools import setup, find_packages

setup(
    name="fintech-review-analytics",
    version="1.0.0",
    description="NLP pipeline for analysing Ethiopian bank customer reviews",
    author="Dagmawi",
    packages=find_packages(exclude=["tests*", "notebooks*", "scripts*"]),
    python_requires=">=3.11",
    install_requires=[
        "pandas>=2.2.0",
        "numpy>=1.26.0",
        "scikit-learn>=1.4.0",
        "transformers>=4.40.0",
        "torch>=2.3.0",
        "google-play-scraper>=1.2.7",
        "SQLAlchemy>=2.0.0",
        "psycopg2-binary>=2.9.9",
        "python-dotenv>=1.0.0",
        "streamlit>=1.35.0",
        "plotly>=5.22.0",
        "matplotlib>=3.8.0",
        "nltk>=3.8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=8.0.0",
            "pytest-cov>=5.0.0",
            "flake8>=7.0.0",
            "black>=24.0.0",
            "isort>=5.13.0",
        ],
        "explainability": [
            "shap>=0.45.0",
        ],
    },
)
