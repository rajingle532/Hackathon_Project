import pytest
from security.pii_masking_service import mask_pii

def test_mask_pii():
    text = "Call me at 9876543210 or email test@example.com"
    masked = mask_pii(text)
    assert "9876543210" not in masked
    assert "test@example.com" not in masked
    assert "[PHONE_NUMBER]" in masked
    assert "[EMAIL]" in masked
