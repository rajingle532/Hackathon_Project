import pytest
from tools.recommendation_tool import recommendation_needed, get_recommendation_context

def test_recommendation_needed():
    assert recommendation_needed("Which crop should I grow?") == True
    assert recommendation_needed("Is it going to rain?") == False

def test_get_recommendation_context(monkeypatch):
    def mock_predict(profile):
        return {"recommended_crops": ["Mock Crop"], "confidence": 0.9, "reasoning": ["Mock reason"]}
        
    monkeypatch.setattr("tools.recommendation_tool.predict_recommended_crops", mock_predict)
    
    ctx = get_recommendation_context("I want to plant something in my loamy soil")
    assert ctx["recommended_crops"] == ["Mock Crop"]
    assert ctx["confidence"] == 0.9
    assert ctx["farm_profile"]["soil_type"] == "loamy"
