import pytest
from memory.mongo_memory_service import load_mongo_memory_context, persist_mongo_memory_context

def test_load_mongo_memory_context_fallback(monkeypatch):
    monkeypatch.setattr("memory.mongo_memory_service.get_farmer_profile_from_mongo", lambda id: None)
    monkeypatch.setattr("memory.mongo_memory_service.get_recent_history_from_mongo", lambda id: None)
    
    ctx = load_mongo_memory_context("1")
    assert ctx is None # Fallback to mock logic

def test_persist_mongo_memory_context_success(monkeypatch):
    monkeypatch.setattr("memory.mongo_memory_service.save_message_to_mongo", lambda m: True)
    monkeypatch.setattr("memory.mongo_memory_service.save_agent_interaction_to_mongo", lambda i: True)
    monkeypatch.setattr("memory.mongo_memory_service.get_farmer_profile_from_mongo", lambda id: {})
    monkeypatch.setattr("memory.mongo_memory_service.update_farmer_profile_in_mongo", lambda id, u: {})
    
    success = persist_mongo_memory_context("1", {"messages": []}, {"intent": "general"})
    assert success == True
