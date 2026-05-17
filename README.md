# SentimentPulse — Social Media Sentiment Analyzer

An end-to-end Machine Learning project for analyzing social media sentiment using Natural Language Processing (NLP), FastAPI, Reddit scraping, and an interactive dashboard interface.

The system collects Reddit posts based on a keyword, preprocesses text data, and predicts sentiment using a trained Support Vector Machine (SVM) classifier.

---

# Features

- Reddit data scraping using Reddit JSON API
- Text preprocessing pipeline
- TF-IDF vectorization
- Sentiment classification using SVM
- FastAPI backend API
- Interactive frontend dashboard
- Sentiment distribution visualization
- Per-post sentiment prediction
- Real sentiment statistics and confidence scores

---

# Technologies Used

## Backend
- Python
- FastAPI
- scikit-learn
- Joblib

## Machine Learning
- Support Vector Machine (LinearSVC)
- TF-IDF Vectorizer

## Frontend
- HTML
- CSS
- JavaScript
- Chart.js

---

# Machine Learning Pipeline

1. Collect dataset
2. Clean and preprocess text
3. Convert text into TF-IDF vectors
4. Train models:
   - Logistic Regression
   - Support Vector Machine (SVM)
5. Evaluate models using:
   - Accuracy
   - Precision
   - Recall
   - F1-score
6. Save the best model using Joblib
7. Serve predictions using FastAPI

---

# Installation

## 1. Clone repository

```bash
git clone https://github.com/fatimIB/Social-Media-Sentiment-Analysis.git
```

## 2. Open project folder

```bash
cd Social-Media-Sentiment-Analysis
```

## 3. Create virtual environment

```bash
python -m venv venv
```

## 4. Activate virtual environment

### Windows
```bash
venv\Scripts\activate
```

### Linux / Mac
```bash
source venv/bin/activate
```

## 5. Install dependencies

```bash
pip install -r requirements.txt
```

---

# Running the Project

## Step 1 — Start FastAPI server

Run:

```bash
uvicorn app.main:app --reload
```

Server will run on:

```bash
http://127.0.0.1:8000
```

---

## Step 2 — Open frontend dashboard

Open the file:

```bash
frontend/dashboard.html
```

in your browser.

You can:
- Enter a keyword
- Analyze Reddit posts
- View sentiment predictions
- Explore sentiment statistics and visualizations
- See relevent posts on Reddit

---

# Dataset

Dataset used for training:
- Twitter Sentiment Dataset

The dataset contains:
- Positive tweets
- Negative tweets
- Neutral tweets

---

# Future Improvements

- Deploy project online
- Add database support
- Add authentication system
- Real-time streaming analysis
- Docker deployment

---

# Authors

Fatima IBOUBKARNE

Amina FARIS

Salma JEGHLOUL

Salma CHLIH

Master's Students in Data Analytics & Artificial Intelligence  
Faculty of Sciences Agadir

---
