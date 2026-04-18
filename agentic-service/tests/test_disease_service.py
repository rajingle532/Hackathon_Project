import pytest
from services.disease_prompt_service import build_disease_prompt

def test_build_disease_prompt():
    ctx = {
        "disease_name": "Leaf Spot",
        "symptoms_detected": ["spots"],
        "confidence": 0.8,
        "requires_escalation": False
    }
    ret_ctx = "Leaf spot requires fungicide."
    prompt = build_disease_prompt("I see spots", ctx, ret_ctx)
    
    assert "I see spots" in prompt
    assert "Leaf Spot" in prompt
    assert "0.8" in prompt
    assert "Leaf spot requires fungicide." in prompt
    assert "ESCALATION REQUIRED" not in prompt

def test_build_disease_prompt_escalation():
    ctx = {
        "disease_name": "Unknown",
        "symptoms_detected": [],
        "confidence": 0.4,
        "requires_escalation": True
    }
    prompt = build_disease_prompt("Help", ctx, "")
    assert "ESCALATION REQUIRED" in prompt
