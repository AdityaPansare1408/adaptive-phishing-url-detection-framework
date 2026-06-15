import re
import unicodedata
from urllib.parse import urlparse

CONFUSION_MAP = {
    '0': 'o', '1': 'l', '3': 'e',
    '@': 'a', '$': 's',
    'I': 'l', 'O': 'o', 'S': 's'
}

KEYWORDS = {
    "login": 0.4, "secure": 0.35, "verify": 0.4,
    "account": 0.35, "update": 0.35,
    "bank": 0.4, "signin": 0.4
}

def normalize(token):
    return "".join(CONFUSION_MAP.get(c, c) for c in token)

def distortion_score(token):
    token_lower = token.lower()
    norm = normalize(token)

    if token_lower == norm.lower():
        return 0

    confusion_used = any(c in CONFUSION_MAP for c in token)

    
    if confusion_used and len(token) > 4:
        changes = sum(1 for a, b in zip(token_lower, norm.lower()) if a != b)
        return min(0.4 + (changes / len(token)), 0.8)

    changes = sum(1 for a, b in zip(token_lower, norm.lower()) if a != b)
    return changes / max(len(token), 1)

def keyword_score(token):
    return KEYWORDS.get(token.lower(), 0)

def unicode_score(token):
    score = 0

    if any(ord(c) > 127 for c in token):
        score += 0.4

    scripts = set()
    for c in token:
        try:
            name = unicodedata.name(c)
            if "CYRILLIC" in name:
                scripts.add("cyrillic")
            elif "LATIN" in name:
                scripts.add("latin")
        except:
            continue

    if len(scripts) > 1:
        score += 0.4

    return min(score, 0.7)

def tokenize(domain):
    return [t for t in re.split(r"[.\-]", domain) if t]

def get_deception_score(url):
    parsed = urlparse(url if url.startswith("http") else "http://" + url)
    domain = parsed.netloc

    if domain.startswith("xn--"):
        return 0.9, ["Punycode domain detected"]

    tokens = tokenize(domain)

    token_scores = []
    explanations = []
    total_keyword_score = 0

    for token in tokens:
        if len(token) <= 2:
            continue

        d = distortion_score(token)
        k = keyword_score(token)
        u = unicode_score(token)

        total_keyword_score += k

        token_score = max(d, u)

        
        if re.search(r'(.)\1{2,}', token):
            token_score = max(token_score, 0.5)
            explanations.append(f"Repeated characters in: {token}")

        token_scores.append(token_score)

        if d > 0:
            explanations.append(f"Distortion detected in: {token}")
        if k > 0:
            explanations.append(f"Keyword detected: {token}")
        if u > 0:
            explanations.append(f"Unicode anomaly in: {token}")

    if not token_scores:
        return 0, []

    
    max_token = max(token_scores)
    avg_token = sum(token_scores) / len(token_scores)
    max_token_score = max(max_token, avg_token * 0.8)

    context_score = min(total_keyword_score, 1.0)
    combined_score = max_token_score + (0.25 * context_score)

    final_score = max(
        max_token_score,
        context_score * 0.8,
        combined_score
    )

    final_score = min(final_score, 0.95)

    return final_score, list(set(explanations))