def detect_scam(text: str):
    keywords = [
        "upi", "refund", "blocked", "verify",
        "urgent", "account", "click", "bank"
    ]

    matched = [k for k in keywords if k in text.lower()]

    return {
        "is_scam": len(matched) > 0,
        "confidence": round(min(0.6 + 0.1 * len(matched), 0.95), 2),
        "matched_keywords": matched
    }
