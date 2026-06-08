try:
    from textblob import TextBlob
except ImportError:
    TextBlob = None


POSITIVE_WORDS = {"amazing", "great", "love", "positive", "excellent", "good", "best", "happy", "trust"}
NEGATIVE_WORDS = {"bad", "hate", "negative", "delay", "frustrating", "poor", "worst", "angry", "scam"}


def sentiment_label(polarity):
    if polarity > 0.1:
        return "Positive"
    if polarity < -0.1:
        return "Negative"
    return "Neutral"


def emotion_from_text(text, polarity):
    lower_text = text.lower()
    if any(word in lower_text for word in ["angry", "bad", "frustrating", "hate", "delay"]):
        return "Frustration"
    if any(word in lower_text for word in ["amazing", "great", "love", "positive", "excellent"]):
        return "Joy"
    if polarity < -0.2:
        return "Concern"
    if polarity > 0.2:
        return "Optimism"
    return "Neutral"


def analyze_sentiments(posts):
    results = []
    for post in posts:
        text = post.get("text", "")
        if TextBlob:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
        else:
            tokens = {word.strip(".,!?").lower() for word in text.split()}
            polarity = (len(tokens & POSITIVE_WORDS) - len(tokens & NEGATIVE_WORDS)) / max(len(tokens), 1)
            subjectivity = min(1, (len(tokens & POSITIVE_WORDS) + len(tokens & NEGATIVE_WORDS)) / max(len(tokens), 1))
        results.append(
            {
                "username": post.get("username", "unknown"),
                "text": text,
                "score": round(polarity, 3),
                "subjectivity": round(subjectivity, 3),
                "label": sentiment_label(polarity),
                "emotion": emotion_from_text(text, polarity),
            }
        )
    return results
