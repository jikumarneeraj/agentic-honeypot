import re

def extract_intelligence(text: str):
    return {
        "upiIds": re.findall(r"[a-zA-Z0-9.\-_]{2,}@[a-zA-Z]{2,}", text),
        "bankAccounts": re.findall(r"\b\d{9,18}\b", text),
        "phishingLinks": re.findall(r"https?://[^\s]+", text),
        "phoneNumbers": re.findall(r"\+?\d{10,13}", text),
        "suspiciousKeywords": [
            w for w in ["urgent", "verify", "blocked", "refund"]
            if w in text.lower()
        ]
    }
