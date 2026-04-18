import pytest
from security.input_sanitizer import sanitize_user_input
from config import settings

def test_sanitize_user_input():
    text = "Hello   World\x00<script>alert(1)</script>"
    sanitized = sanitize_user_input(text)
    assert "  " not in sanitized
    assert "\x00" not in sanitized
    assert "<script>" not in sanitized
    assert "Hello World" in sanitized
