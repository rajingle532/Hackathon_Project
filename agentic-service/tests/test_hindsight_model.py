import pytest
from models.hindsight_model import normalize_hindsight_log, validate_hindsight_log

def test_normalize_hindsight_log():
    raw = {"interaction_id": "123", "outcome_status": "successful"}
    norm = normalize_hindsight_log(raw)
    assert norm["interaction_id"] == "123"
    assert norm["outcome_status"] == "successful"
    assert "timestamp" in norm

def test_validate_hindsight_log():
    assert validate_hindsight_log({"interaction_id": "123"}) == True
    assert validate_hindsight_log({"outcome_status": "successful"}) == False
