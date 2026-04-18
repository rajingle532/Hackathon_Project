import pytest
from models.feedback_model import normalize_feedback, validate_feedback

def test_normalize_feedback():
    raw = {"interaction_id": "123", "feedback_type": "thumbs_up"}
    norm = normalize_feedback(raw)
    assert norm["interaction_id"] == "123"
    assert norm["feedback_type"] == "thumbs_up"
    assert "timestamp" in norm

def test_validate_feedback():
    assert validate_feedback({"interaction_id": "123", "feedback_type": "thumbs_up"}) == True
    assert validate_feedback({"interaction_id": "123"}) == False
    assert validate_feedback(None) == False
