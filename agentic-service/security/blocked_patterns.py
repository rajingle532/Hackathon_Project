# Centralized blocked patterns if needed
import re

MALICIOUS_PAYLOAD_PATTERNS = [
    r"<script.*?>.*?</script>",
    r"javascript:",
    r"vbscript:",
    r"onload=",
    r"onerror="
]
