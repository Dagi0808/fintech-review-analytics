CREATE TABLE banks (
    bank_id SERIAL PRIMARY KEY,
    bank_name VARCHAR(100) NOT NULL,
    app_name VARCHAR(150) NOT NULL
);

CREATE TABLE reviews (
    review_id SERIAL PRIMARY KEY,
    bank_id INTEGER REFERENCES banks(bank_id),
    review_text TEXT,
    rating INTEGER,
    review_date DATE,
    sentiment_label VARCHAR(20),
    sentiment_score DOUBLE PRECISION,
    identified_theme VARCHAR(100),
    source VARCHAR(50)
);