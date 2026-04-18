import pytest
from models.agent_interaction_model import normalize_agent_interaction, validate_agent_interaction

def test_normalize_agent_interaction():
    interaction = {"farmer_id": 123, "intent": "general"}
    norm = normalize_agent_interaction(interaction)
    assert norm["farmer_id"] == "123"
    assert norm["intent"] == "general"
    assert "timestamp" in norm

def test_validate_agent_interaction():
    assert validate_agent_interaction({"farmer_id": "1"}) == True
    assert validate_agent_interaction({"intent": "general"}) == False
