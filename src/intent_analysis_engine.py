import re

SUSPICIOUS_KEYWORDS = [
    "login", "verify", "update", "secure",
    "account", "bank", "signin", "confirm"
]

def tokenize(url):
    url = url.lower()
    domain = url.replace("http://", "").replace("https://", "").split("/")[0]
    return re.split(r"[.\-]", domain)

def compute_intent_score(url):
    tokens = tokenize(url)

    keyword_hits = [t for t in tokens if t in SUSPICIOUS_KEYWORDS]
    count = len(keyword_hits)

    if count == 0:
        score = 0
    elif count == 1:
        score = 0.3
    elif count == 2:
        score = 0.55
    else:
        score = 0.75

    reasons = []
    for kw in keyword_hits:
        reasons.append(f"Keyword detected: {kw}")

    if count >= 2:
        reasons.append("Multiple suspicious keywords detected")

    return score, reasons