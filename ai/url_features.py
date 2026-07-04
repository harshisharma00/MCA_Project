"""Hand-crafted feature extraction for phishing URL detection.

We deliberately avoid heavy NLP — a small set of well-understood
lexical / structural features (length, character counts, suspicious
keywords, risky TLDs) is interpretable for the viva and trains in
under a second on ~1500 URLs.
"""
import re
from urllib.parse import urlparse

SUSPICIOUS_KEYWORDS = [
    "login", "verify", "account", "secure", "update", "confirm",
    "bank", "wallet", "signin", "password", "billing", "support",
    "free", "bonus", "gift", "prize", "claim", "win", "urgent",
    "auth", "validate", "recover", "unlock", "reset",
]

RISKY_TLDS = {
    "tk", "ml", "ga", "cf", "gq", "xyz", "top", "club", "click",
    "loan", "work", "country", "men", "win", "review", "stream",
    "download", "racing", "party", "trade", "date",
}

IP_RE = re.compile(
    r"^(?:\d{1,3}\.){3}\d{1,3}$"
)
URL_RE = re.compile(
    r"\b((?:https?://|www\.)[^\s,]+)",
    re.IGNORECASE,
)

FEATURE_NAMES = [
    "url_length",
    "host_length",
    "path_length",
    "n_dots",
    "n_dashes",
    "n_at",
    "n_question_marks",
    "n_equals",
    "n_double_slash",
    "has_at",
    "has_ip_host",
    "uses_https",
    "n_suspicious_keywords",
    "has_risky_tld",
    "n_digits_in_host",
    "subdomain_depth",
]


def _safe_parse(url: str):
    if "://" not in url:
        url = "http://" + url
    return urlparse(url)


def extract_features(url: str) -> dict:
    """Return a dict of numeric features for one URL."""
    url = (url or "").strip()
    parsed = _safe_parse(url)
    host = parsed.hostname or ""
    path = parsed.path or ""

    lower_url = url.lower()
    lower_host = host.lower()

    n_keywords = sum(1 for kw in SUSPICIOUS_KEYWORDS if kw in lower_url)

    tld = lower_host.rsplit(".", 1)[-1] if "." in lower_host else ""

    return {
        "url_length": len(url),
        "host_length": len(host),
        "path_length": len(path),
        "n_dots": url.count("."),
        "n_dashes": url.count("-"),
        "n_at": url.count("@"),
        "n_question_marks": url.count("?"),
        "n_equals": url.count("="),
        "n_double_slash": max(0, url.count("//") - 1),
        "has_at": int("@" in url),
        "has_ip_host": int(bool(IP_RE.match(host))),
        "uses_https": int(parsed.scheme == "https"),
        "n_suspicious_keywords": n_keywords,
        "has_risky_tld": int(tld in RISKY_TLDS),
        "n_digits_in_host": sum(c.isdigit() for c in host),
        "subdomain_depth": max(0, lower_host.count(".") - 1),
    }


def extract_feature_vector(url: str) -> list:
    """Return features as an ordered list (for sklearn input)."""
    features = extract_features(url)
    return [features[name] for name in FEATURE_NAMES]


def find_urls_in_text(text: str) -> list[str]:
    """Pull every plausible URL out of a chat message."""
    return [m.group(1).rstrip(".,);!?") for m in URL_RE.finditer(text or "")]
