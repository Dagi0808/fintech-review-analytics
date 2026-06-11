# 📊 Fintech Bank Review Analytics Project

## 🧠 Overview

This project is an end-to-end **data engineering and analytics pipeline** built to analyze customer reviews from Ethiopian banks: **CBE, BOA, and DASHEN**.

It combines **PostgreSQL, Python, sentiment analysis, and data visualization** to extract business insights from 1,502 real customer reviews.

The goal is to understand customer satisfaction, identify pain points, and provide actionable recommendations for improving banking services.

---

## 🎯 Objectives

- Build a structured relational database using PostgreSQL
- Load and manage 1,502 customer reviews
- Perform sentiment analysis on banking feedback
- Analyze customer satisfaction across banks
- Identify key complaint themes
- Generate data-driven business recommendations

---

## 🏗️ Tech Stack

- **Python** (Pandas, SQLAlchemy, Matplotlib, Seaborn)
- **PostgreSQL 16**
- **Jupyter Notebook**
- **SQL**
- **Git & GitHub**

---

## 🗄️ Database Design

### 📌 Tables

#### banks
- bank_id (Primary Key)
- bank_name
- app_name

#### reviews
- review_id (Primary Key)
- bank_id (Foreign Key)
- review_text
- rating
- review_date
- sentiment_label
- sentiment_score
- identified_theme
- source

---

## 🔄 Data Pipeline

1. Raw review dataset collected and cleaned
2. Sentiment analysis applied to reviews
3. Data transformed and structured
4. Loaded into PostgreSQL (1,502 records)
5. SQL queries used for validation
6. Exploratory Data Analysis performed in Jupyter Notebook

---

## 📊 Key Insights

### 🏦 Bank Performance Comparison

- **DASHEN Bank**
  - Highest customer satisfaction
  - Highest average rating (~3.7)
  - Strong positive sentiment

- **BOA (Bank of Abyssinia)**
  - Moderate performance
  - Balanced sentiment distribution
  - Average rating (~3.2)

- **CBE (Commercial Bank of Ethiopia)**
  - Lowest performance
  - Highest number of complaints
  - Needs improvement in digital services

---

### 😊 Sentiment Analysis

- Majority of reviews are **positive**
- Negative reviews highlight operational inefficiencies
- High confidence sentiment scores (>0.9) indicate reliable classification

---

### 🧠 Customer Pain Points

Most common issues identified:

- Mobile banking instability
- Transaction delays
- Login/authentication failures
- Poor customer service response
- ATM and network downtime

---

## 📈 Business Recommendations

### For All Banks:
- Improve mobile banking performance and stability
- Reduce transaction processing delays
- Strengthen customer support systems

### For CBE:
- Priority focus on digital transformation
- Improve system reliability and app stability

### For BOA:
- Enhance service consistency and uptime

### For DASHEN:
- Maintain performance advantage
- Improve UX and feature set in mobile banking

---

## 📊 Visual Analysis

The project includes:
- Sentiment distribution charts
- Bank comparison visualizations
- Average rating analysis
- Customer complaint theme analysis

(All visualizations are available in the Jupyter Notebook)

---

## 📁 Project Structure
fintech-review-analytics/
│
├── data/                     # Raw and processed datasets
│
├── notebooks/               # EDA and experiments
│   └── task4_eda.ipynb
│
├── src/                     # Core pipeline code
│   ├── db_insert.py
│   ├── sentiment_analysis.py
│   ├── theme_extraction.py
│
├── sql/                     # Database schema
│   └── schema.sql
│
├── scripts/                # Utility / automation scripts
│
├── tests/                  # Validation and testing scripts
│
├── .env                    # Environment variables (not pushed to GitHub)
├── requirements.txt        # Dependencies (IMPORTANT for portfolio)
├── README.md               # Project documentation
│
└── .gitignore
