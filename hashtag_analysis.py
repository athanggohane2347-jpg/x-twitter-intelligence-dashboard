import re
from collections import Counter


HASHTAG_PATTERN = re.compile(r"#\w+")


def analyze_hashtags(posts, limit=10):
    hashtags = []
    for post in posts:
        hashtags.extend(tag.lower() for tag in HASHTAG_PATTERN.findall(post.get("text", "")))
    return [{"tag": tag, "count": count} for tag, count in Counter(hashtags).most_common(limit)]
