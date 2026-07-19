import csv
from functools import wraps
from pathlib import Path
from flask import Blueprint, Response, current_app, flash, redirect, render_template, request, session, url_for
from werkzeug.utils import secure_filename

from sentiment import analyze_sentiments
from spam_detection import detect_spam
from fake_account_detection import detect_fake_accounts
from hashtag_analysis import analyze_hashtags
from keyword_analysis import analyze_keywords, build_wordcloud_image
from database import get_recent_analyses, save_analysis
from csv_export import serialize_csv_row

dashboard_bp = Blueprint("dashboard", __name__)
ALLOWED_EXTENSIONS = {"csv"}


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if not session.get("user_id"):
            flash("Please log in first.", "warning")
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)

    return wrapped_view


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def sample_posts():
    return [
        {
            "username": "insight_user",
            "text": "Amazing product launch today. The response from users is very positive!",
            "followers": 1520,
            "following": 410,
            "account_age_days": 730,
            "posts_count": 184,
        },
        {
            "username": "promo_fast_001",
            "text": "Win free cash now. Click this link and claim your reward!",
            "followers": 12,
            "following": 940,
            "account_age_days": 7,
            "posts_count": 4,
        },
        {
            "username": "marketwatcher",
            "text": "New updates in AI policy are trending with #AI #Technology #Innovation.",
            "followers": 820,
            "following": 350,
            "account_age_days": 580,
            "posts_count": 120,
        },
        {
            "username": "feedbackdesk",
            "text": "The service delay was frustrating and disappointing for many customers.",
            "followers": 430,
            "following": 280,
            "account_age_days": 340,
            "posts_count": 76,
        },
        {
            "username": "dailytrend",
            "text": "Creators are discussing #Marketing #SocialMedia and brand trust today.",
            "followers": 2500,
            "following": 600,
            "account_age_days": 1000,
            "posts_count": 330,
        },
    ]


def read_posts_from_csv(file_path):
    posts = []
    with open(file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            text = row.get("text") or row.get("tweet") or row.get("post") or ""
            if not text.strip():
                continue
            posts.append(
                {
                    "username": row.get("username", "unknown"),
                    "text": text.strip(),
                    "followers": int(float(row.get("followers", 0) or 0)),
                    "following": int(float(row.get("following", 0) or 0)),
                    "account_age_days": int(float(row.get("account_age_days", 30) or 30)),
                    "posts_count": int(float(row.get("posts_count", 1) or 1)),
                }
            )
    return posts


def analyze_posts(posts):
    sentiment = analyze_sentiments(posts)
    spam = detect_spam(posts)
    fake = detect_fake_accounts(posts)
    hashtags = analyze_hashtags(posts)
    keywords = analyze_keywords(posts)
    wordcloud_file = build_wordcloud_image([post["text"] for post in posts])

    total = len(posts)
    positive = sum(1 for item in sentiment if item["label"] == "Positive")
    negative = sum(1 for item in sentiment if item["label"] == "Negative")
    neutral = total - positive - negative
    spam_count = sum(1 for item in spam if item["is_spam"])
    fake_count = sum(1 for item in fake if item["is_fake"])

    summary = {
        "total_posts": total,
        "positive_count": positive,
        "negative_count": negative,
        "neutral_count": neutral,
        "spam_count": spam_count,
        "fake_count": fake_count,
        "positive_percent": round((positive / total) * 100, 1) if total else 0,
        "negative_percent": round((negative / total) * 100, 1) if total else 0,
        "neutral_percent": round((neutral / total) * 100, 1) if total else 0,
        "spam_percent": round((spam_count / total) * 100, 1) if total else 0,
        "fake_percent": round((fake_count / total) * 100, 1) if total else 0,
    }

    return {
        "posts": posts,
        "summary": summary,
        "sentiment": sentiment,
        "spam": spam,
        "fake": fake,
        "hashtags": hashtags,
        "keywords": keywords,
        "wordcloud_file": wordcloud_file,
    }


@dashboard_bp.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    filename = "sample-data"
    posts = sample_posts()

    if request.method == "POST":
        uploaded_file = request.files.get("csv_file")
        if not uploaded_file or uploaded_file.filename == "":
            flash("Please choose a CSV file.", "warning")
            return redirect(url_for("dashboard.dashboard"))

        if not allowed_file(uploaded_file.filename):
            flash("Only CSV files are supported.", "danger")
            return redirect(url_for("dashboard.dashboard"))

        filename = secure_filename(uploaded_file.filename)
        save_path = Path(current_app.config["UPLOAD_FOLDER"]) / filename
        uploaded_file.save(save_path)

        try:
            posts = read_posts_from_csv(save_path)
            if not posts:
                flash("CSV must contain a text, tweet, or post column.", "danger")
                return redirect(url_for("dashboard.dashboard"))
        except Exception as error:
            flash(f"Could not read CSV: {error}", "danger")
            return redirect(url_for("dashboard.dashboard"))

    results = analyze_posts(posts)
    session["latest_posts"] = posts
    save_analysis(session["user_id"], filename, results["summary"])
    recent_analyses = get_recent_analyses(session["user_id"])

    return render_template(
        "dashboard.html",
        results=results,
        recent_analyses=recent_analyses,
        user_name=session.get("user_name", "User"),
    )


@dashboard_bp.route("/download/csv")
@login_required
def download_csv():
    posts = session.get("latest_posts") or sample_posts()
    results = analyze_posts(posts)

    def generate():
        yield serialize_csv_row(
            ["username", "text", "sentiment", "spam_risk", "fake_risk"]
        )
        for index, post in enumerate(results["posts"]):
            yield serialize_csv_row(
                [
                    post["username"],
                    post["text"],
                    results["sentiment"][index]["label"],
                    results["spam"][index]["risk_level"],
                    results["fake"][index]["risk_level"],
                ]
            )

    return Response(
        generate(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=social_media_analysis.csv"},
    )
