import pytest
from security.request_validator import validate_chat_request
from config import settings

def test_validate_chat_request(monkeypatch):
    monkeypatch.setattr(settings, "MAX_MESSAGE_LENGTH", 10)
    
    payload = {"message": "hello"}
    is_valid, msg = validate_chat_request(payload)
    assert is_valid is True
    
    payload_long = {"message": "this is a very long message"}
    is_valid, msg = validate_chat_request(payload_long)
    assert is_valid is False
