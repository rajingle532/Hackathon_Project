import pytest
from services.recommendation_prompt_service import build_recommendation_prompt

def test_build_recommendation_prompt():
    profile = {"soil_type": "loamy", "season": "kharif", "irrigation_available": True}
    ctx = {"recommended_crops": ["Rice"], "confidence": 0.8, "reasoning": ["Needs water"]}
    
    prompt = build_recommendation_prompt("What should I grow?", profile, ctx, "RAG Context")
    assert "What should I grow?" in prompt
    assert "loamy" in prompt
    assert "Rice" in prompt
    assert "0.8" in prompt
    assert "RAG Context" in prompt
    assert "WARNING" not in prompt

def test_build_recommendation_prompt_warning():
    profile = {}
    ctx = {"recommended_crops": ["Wheat"], "confidence": 0.4} # Low confidence
    
    prompt = build_recommendation_prompt("Help", profile, ctx, "")
    assert "WARNING:" in prompt
