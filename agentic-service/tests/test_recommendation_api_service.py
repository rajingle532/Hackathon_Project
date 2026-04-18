import pytest
from services.recommendation_api_service import predict_recommended_crops
from utils.recommendation_constants import FALLBACK_CROPS

def test_predict_recommended_crops_loamy_kharif():
    profile = {"soil_type": "loamy", "season": "kharif"}
    res = predict_recommended_crops(profile)
    assert res["success"] == True
    assert "Rice" in res["recommended_crops"]
    assert res["confidence"] == 0.85

def test_predict_recommended_crops_fallback(monkeypatch):
    import config
    monkeypatch.setattr(config.settings, "ENABLE_RECOMMENDATION_FALLBACK", False)
    
    # We will mock an exception if we need to test the exception block,
    # but the current mock always succeeds unless we throw.
    # To test fallback reasoning, we can just ensure the structure matches what's returned.
    profile = {"soil_type": "unknown", "season": "unknown"}
    res = predict_recommended_crops(profile)
    assert "Pulses" in res["recommended_crops"] # Fall through logic

    # Test error
    def mock_fail(*args, **kwargs):
        raise ValueError("API Down")
    monkeypatch.setattr("services.recommendation_api_service.settings.DEFAULT_SOIL_TYPE", mock_fail) # trigger error
    
    res = predict_recommended_crops(profile)
    assert res["confidence"] == 0.40
    assert res["recommended_crops"] == FALLBACK_CROPS
