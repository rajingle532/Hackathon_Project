import pytest
from memory.memory_service import load_memory_context, enrich_profile_from_message, save_interaction_context

def test_load_memory_context():
    ctx = load_memory_context("test_mem_1")
    assert "profile" in ctx
    assert "history" in ctx

def test_enrich_profile_from_message():
    updates = enrich_profile_from_message("I live in punjab and grow wheat", {})
    assert updates.get("location") == "Punjab"
    assert "Wheat" in updates.get("crops_grown", [])

def test_save_interaction_context(monkeypatch):
    class MockMessage:
        content = "hello from punjab"
        
    state = {"messages": [MockMessage()]}
    response = {"intent": "general", "reply": "hi", "metadata": {"soil_type": "loamy"}}
    
    save_interaction_context("test_mem_2", state, response)
    
    ctx = load_memory_context("test_mem_2")
    assert ctx["profile"]["soil_type"] == "loamy"
    assert ctx["profile"]["location"] == "Punjab"
