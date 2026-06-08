def detect_fake_accounts(posts):
    results = []
    for post in posts:
        followers = int(post.get("followers", 0) or 0)
        following = int(post.get("following", 0) or 0)
        account_age_days = int(post.get("account_age_days", 30) or 30)
        posts_count = int(post.get("posts_count", 1) or 1)

        score = 0
        reasons = []

        if account_age_days < 30:
            score += 30
            reasons.append("Very new account")
        if followers < 25 and following > 300:
            score += 30
            reasons.append("Low followers with high following")
        if posts_count < 5:
            score += 20
            reasons.append("Very low posting history")
        if followers == 0:
            score += 20
            reasons.append("No followers")

        score = min(score, 100)
        if score >= 70:
            risk_level = "High"
        elif score >= 35:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        results.append(
            {
                "username": post.get("username", "unknown"),
                "is_fake": score >= 50,
                "score": score,
                "risk_level": risk_level,
                "reasons": reasons or ["Account behavior appears normal"],
            }
        )
    return results
