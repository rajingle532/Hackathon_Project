import pytest
from security.auth_service import authenticate_request
from config import settings

def test_authenticate_request_no_auth(monkeypatch):
    monkeypatch.setattr(settings, "ENABLE_AUTH", False)
    res = authenticate_request()
    assert res["authenticated"] is True

def test_authenticate_request_api_key(monkeypatch):
    monkeypatch.setattr(settings, "ENABLE_AUTH", True)
    monkeypatch.setattr(settings, "ENABLE_API_KEYS", True)
    monkeypatch.setattr(settings, "VALID_API_KEYS", "test_key")
    
    res = authenticate_request(api_key="test_key")
    assert res["authenticated"] is True
    assert res["auth_type"] == "api_key"
