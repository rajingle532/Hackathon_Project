import pytest
from memory.context_builder import build_profile_context, build_history_context, build_memory_context

def test_build_profile_context():
    profile = {
        "location": "Punjab",
        "soil_type": "loamy",
        "crops_grown": ["Wheat", "Rice"]
    }
    ctx = build_profile_context(profile)
    assert "Location: Punjab" in ctx
    assert "Soil Type: loamy" in ctx
    assert "Wheat, Rice" in ctx

def test_build_history_context():
    history = [{"role": "user", "content": "hello"}]
    ctx = build_history_context(history)
    assert "User: hello" in ctx

def test_build_memory_context():
    profile = {"location": "Delhi"}
    history = [{"role": "user", "content": "hi"}]
    ctx = build_memory_context(profile, history)
    
    assert "profile_context" in ctx
    assert "history_context" in ctx
    assert "Location: Delhi" in ctx["profile_context"]
    assert "User: hi" in ctx["history_context"]
