SPAM_KEYWORDS = {
    "free",
    "win",
    "cash",
    "prize",
    "click",
    "claim",
    "reward",
    "limited offer",
    "guaranteed",
    "investment",
    "urgent",
}


def detect_spam(posts):
    results = []
    for post in posts:
        text = post.get("text", "").lower()
        matched = [keyword for keyword in SPAM_KEYWORDS if keyword in text]
        link_count = text.count("http") + text.count("www.")
        repeated_symbols = text.count("!!!") + text.count("???")
        score = min(100, len(matched) * 18 + link_count * 20 + repeated_symbols * 10)

        if score >= 60:
            risk_level = "High"
        elif score >= 30:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        results.append(
            {
                "username": post.get("username", "unknown"),
                "is_spam": score >= 45,
                "score": score,
                "risk_level": risk_level,
                "reasons": matched or ["No strong spam pattern detected"],
            }
        )
    return results
