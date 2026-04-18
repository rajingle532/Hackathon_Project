# Simple regex patterns for PII detection
PII_PATTERNS = {
    "PHONE_NUMBER": r"\b\d{10}\b",
    "AADHAAR": r"\b\d{4}\s?\d{4}\s?\d{4}\b",
    "EMAIL": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    "BANK_ACCOUNT": r"\b\d{9,18}\b"
}
