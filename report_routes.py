from datetime import datetime
from pathlib import Path
from flask import Blueprint, current_app, flash, redirect, send_file, session, url_for

from sentiment import analyze_sentiments
from spam_detection import detect_spam
from fake_account_detection import detect_fake_accounts
from dashboard_routes import login_required, sample_posts

report_bp = Blueprint("reports", __name__)


@report_bp.route("/download/pdf")
@login_required
def download_pdf():
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
    except ImportError:
        flash("PDF generation requires reportlab. Run: pip install -r requirements.txt", "danger")
        return redirect(url_for("dashboard.dashboard"))

    posts = session.get("latest_posts") or sample_posts()
    sentiment = analyze_sentiments(posts)
    spam = detect_spam(posts)
    fake = detect_fake_accounts(posts)

    filename = f"social_media_report_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.pdf"
    report_path = Path(current_app.config["REPORT_FOLDER"]) / filename

    pdf = canvas.Canvas(str(report_path), pagesize=letter)
    width, height = letter
    y = height - 60

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(50, y, "AI-Powered Social Media Intelligence Report")
    y -= 30

    pdf.setFont("Helvetica", 10)
    pdf.drawString(50, y, f"Generated for: {session.get('user_name', 'User')}")
    y -= 18
    pdf.drawString(50, y, f"Generated on: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
    y -= 35

    positive = sum(1 for item in sentiment if item["label"] == "Positive")
    negative = sum(1 for item in sentiment if item["label"] == "Negative")
    neutral = len(posts) - positive - negative
    spam_count = sum(1 for item in spam if item["is_spam"])
    fake_count = sum(1 for item in fake if item["is_fake"])

    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(50, y, "Summary")
    y -= 22
    pdf.setFont("Helvetica", 11)
    for line in [
        f"Total Posts: {len(posts)}",
        f"Positive: {positive}",
        f"Negative: {negative}",
        f"Neutral: {neutral}",
        f"Spam Detected: {spam_count}",
        f"Fake or Risky Accounts: {fake_count}",
    ]:
        pdf.drawString(65, y, line)
        y -= 18

    y -= 16
    pdf.setFont("Helvetica-Bold", 13)
    pdf.drawString(50, y, "Analyzed Posts")
    y -= 22
    pdf.setFont("Helvetica", 9)

    for index, post in enumerate(posts, start=1):
        if y < 80:
            pdf.showPage()
            y = height - 60
            pdf.setFont("Helvetica", 9)

        text = post["text"][:88] + ("..." if len(post["text"]) > 88 else "")
        pdf.drawString(60, y, f"{index}. @{post['username']} - {text}")
        y -= 14

    pdf.save()
    return send_file(report_path, as_attachment=True)
