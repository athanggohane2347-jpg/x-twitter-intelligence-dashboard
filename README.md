# 🚀 AI-Powered X/Twitter Social Media Intelligence Dashboard

> Transform raw social media data into actionable intelligence using AI, Machine Learning, and Interactive Analytics.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Flask](https://img.shields.io/badge/Flask-Web_App-black)
![SQLite](https://img.shields.io/badge/SQLite-Database-blue)
![Machine Learning](https://img.shields.io/badge/Machine-Learning-green)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple)
![Chart.js](https://img.shields.io/badge/Chart.js-Analytics-orange)

---

## 📌 Project Overview

The **AI-Powered X/Twitter Social Media Intelligence Dashboard** is a full-stack analytics platform designed to monitor, analyze, and visualize social media data.

Built using **Flask, SQLite, Pandas, NLTK, TextBlob, Scikit-Learn, Bootstrap 5, and Chart.js**, the dashboard provides advanced social media intelligence including:

* Sentiment Analysis
* Hashtag Tracking
* Trending Keyword Detection
* Fake Account Identification
* Spam Detection
* Word Cloud Generation
* PDF Reporting
* Interactive Analytics Dashboards

This project modernizes traditional social media analytics by combining **Artificial Intelligence**, **Machine Learning**, and **Data Visualization** into a single platform.

---

# ✨ Key Features

## 🔐 Authentication System

* User Registration
* Secure Login
* Session Management
* Protected Dashboard Access

---

## 📊 Social Media Analytics

### 😊 Sentiment Analysis

Analyze social media posts and classify them as:

* Positive
* Negative
* Neutral

Features:

* Sentiment Score
* Emotion Classification
* Pie Chart Visualization
* Trend Analysis

---

### #️⃣ Hashtag Intelligence

Discover:

* Most Used Hashtags
* Trending Topics
* Engagement Opportunities

---

### 🔥 Trending Keyword Detection

Automatically identify:

* Viral Keywords
* Trending Discussions
* Popular Topics

---

### ☁️ Word Cloud Generation

Generate visual word clouds from uploaded datasets to instantly identify dominant discussion themes.

---

## 🛡️ Risk Analysis Engine

### 🤖 Fake Account Detection

Detect suspicious accounts using:

* Followers/Following Ratio
* Account Age
* Activity Patterns
* Posting Behavior

---

### 🚫 Spam Detection

Identify:

* Spam Posts
* Promotional Bots
* Suspicious Content

---

## 📁 Data Management

### CSV Upload

Upload datasets containing:

* Tweets
* Posts
* User Data

Supported Fields:

```csv
username,text,followers,following,account_age_days,posts_count
```

### Xquik Export Import

Reviewed X/Twitter exports from Xquik can be converted into the same CSV upload
schema before analysis:

```bash
python xquik_csv.py examples/xquik-posts.jsonl -o uploads/xquik_posts.csv
```

The converter accepts JSON, JSONL, NDJSON, or CSV rows and maps common Xquik
post fields such as `text`, `tweetText`, `replyText`, `content`, `username`,
`author.username`, `followersCount`, `followingCount`, and `statusesCount` into
the dashboard's upload columns. After conversion, upload
`uploads/xquik_posts.csv` from the dashboard to run the existing sentiment,
hashtag, spam, fake-account, word-cloud, CSV export, and PDF report workflow.

Source: https://github.com/Xquik-dev/x-twitter-scraper

Xquik is an independent third-party service. Not affiliated with X Corp.
"Twitter" and "X" are trademarks of X Corp.

### CSV Export

Export processed analytics results.

---

### 📄 PDF Report Generation

Generate professional downloadable reports containing:

* Sentiment Results
* Risk Analysis
* Hashtag Statistics
* Keyword Trends

---

## 🌙 Modern User Experience

### Dashboard Features

* Glassmorphism UI
* Dark Mode
* Responsive Design
* Interactive Charts
* Animated Cards
* Mobile Friendly Layout
* SaaS Inspired Interface

---

# 🛠️ Technology Stack

## Frontend

* HTML5
* CSS3
* JavaScript
* Bootstrap 5
* Chart.js

## Backend

* Python Flask

## Database

* SQLite

## Machine Learning & NLP

* Pandas
* NLTK
* TextBlob
* Scikit-Learn
* WordCloud

## Reporting

* ReportLab

---

# 📂 Project Structure

```bash
x-twitter-intelligence-dashboard/

├── app.py
├── database.py
├── auth_routes.py
├── dashboard_routes.py
├── report_routes.py
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   └── dashboard.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   └── js/
│       ├── dashboard.js
│       └── theme.js
│
├── sentiment.py
├── spam_detection.py
├── fake_account_detection.py
├── hashtag_analysis.py
├── keyword_analysis.py
│
├── uploads/
├── reports/
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/x-twitter-intelligence-dashboard.git

cd x-twitter-intelligence-dashboard
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Download NLP Resources

```bash
python -m textblob.download_corpora
```

### Run Application

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

---

# 📸 Project Screenshots

## 🏠 Landing Page

![Landing Page](screenshots/Screenshot%202026-06-09%20012408.png)

## 🔐 User Registration

![Registration Page](screenshots/Screenshot%202026-06-09%20012422.png)

## 📊 Dashboard Overview

![Dashboard](screenshots/Screenshot%202026-06-09%20012538.png)

## 📈 Analytics & Intelligence

![Analytics](screenshots/Screenshot%202026-06-09%20012624.png)

---

# 📈 Sample Dataset

```csv
username,text,followers,following,account_age_days,posts_count
brand_user,"Great update today with #AI and #Marketing",1200,300,600,150
promo_bot,"Win free cash now click this link",8,900,5,2
```

---

# 🎯 Future Enhancements

* Real-Time X API Integration
* AI Chat Assistant
* Predictive Trend Forecasting
* Multi-Platform Social Media Monitoring
* Advanced Machine Learning Models
* Live Streaming Analytics

---

# 👨‍💻 Author

**Athang Gohane**

Passionate about:

* Full Stack Development
* Artificial Intelligence
* Data Analytics
* Machine Learning
* Modern Web Applications

---

## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.
