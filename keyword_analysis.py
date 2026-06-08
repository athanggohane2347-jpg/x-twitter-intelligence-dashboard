import re
from collections import Counter
from pathlib import Path

STOPWORDS = {
    "the", "and", "for", "with", "this", "that", "are", "was", "from", "you",
    "your", "have", "has", "today", "now", "new", "our", "their", "about",
    "into", "more", "many", "will", "just", "than", "post", "tweet"
}


def tokenize(text):
    return [
        word.lower()
        for word in re.findall(r"\b[a-zA-Z]{3,}\b", text)
        if word.lower() not in STOPWORDS
    ]


def analyze_keywords(posts, limit=12):
    words = []
    for post in posts:
        words.extend(tokenize(post.get("text", "")))
    return [{"word": word, "count": count} for word, count in Counter(words).most_common(limit)]


def build_wordcloud_image(texts):
    try:
        from wordcloud import WordCloud
    except ImportError:
        return None

    text = " ".join(texts).strip()
    if not text:
        return None

    output_dir = Path("static/images")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "wordcloud.png"

    cloud = WordCloud(
        width=1100,
        height=520,
        background_color="white",
        colormap="viridis",
        max_words=80,
    ).generate(text)
    cloud.to_file(output_file)
    return "images/wordcloud.png"
