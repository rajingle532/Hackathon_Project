import pytest
from security.api_key_service import validate_api_key
from config import settings

def test_validate_api_key(monkeypatch):
    monkeypatch.setattr(settings, "ENABLE_API_KEYS", True)
    monkeypatch.setattr(settings, "VALID_API_KEYS", "key1,key2")
    
    assert validate_api_key("key1") is True
    assert validate_api_key("key3") is False
