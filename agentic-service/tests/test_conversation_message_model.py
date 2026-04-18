import pytest
from models.conversation_message_model import normalize_conversation_message, validate_conversation_message

def test_normalize_conversation_message():
    msg = {"farmer_id": 123, "role": "user", "content": "hi"}
    norm = normalize_conversation_message(msg)
    assert norm["farmer_id"] == "123"
    assert norm["role"] == "user"
    assert "timestamp" in norm

def test_validate_conversation_message():
    assert validate_conversation_message({"farmer_id": "1", "role": "user"}) == True
    assert validate_conversation_message({"farmer_id": "1"}) == False
