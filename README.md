# AI-Powered Social Media Intelligence Dashboard

A modern Flask, Bootstrap 5, Chart.js, SQLite, and Python analytics project that rebuilds an old R Shiny Twitter dashboard as a professional social media intelligence product.

## Features

- Modern landing page
- Login and registration
- User dashboard
- CSV upload
- Sentiment analysis
- Hashtag analysis
- Trending keywords
- Word cloud
- Fake account detection
- Spam detection
- CSV export
- PDF report generation
- Dark mode
- Responsive SaaS dashboard UI

## Tech Stack

- Frontend: HTML5, CSS3, JavaScript, Bootstrap 5, Chart.js
- Backend: Python Flask
- Database: SQLite
- Analytics: Pandas, NLTK, TextBlob, Scikit-learn
- Reports: ReportLab

## Setup

```bash
cd social-media-dashboard
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m textblob.download_corpora
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## CSV Format

Upload a CSV with at least one of these text columns:

```text
text
tweet
post
```

Optional account columns:

```text
username, followers, following, account_age_days, posts_count
```

Example:

```csv
username,text,followers,following,account_age_days,posts_count
brand_user,"Great update today with #AI and #Marketing",1200,300,600,150
promo_bot,"Win free cash now click this link",8,900,5,2
```

## GitHub Commands

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/social-media-dashboard.git
git push -u origin main
```

## Notes

`database.db` is created automatically when the Flask app starts.
