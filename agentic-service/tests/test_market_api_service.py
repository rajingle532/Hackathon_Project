import pytest
from services.market_api_service import get_market_price
from utils.market_constants import FALLBACK_PRICE_TREND

def test_get_market_price_wheat():
    profile = {"commodity_name": "Wheat", "market_location": "Delhi"}
    res = get_market_price(profile)
    assert res["success"] == True
    assert res["market_price"] == "₹2450/quintal"
    assert res["price_trend"] == "rising"

def test_get_market_price_fallback(monkeypatch):
    import config
    monkeypatch.setattr(config.settings, "ENABLE_MARKET_FALLBACK", False)
    
    def mock_fail(*args, **kwargs):
        raise ValueError("API Down")
    # Trigger exception via mock
    monkeypatch.setattr("services.market_api_service.settings.DEFAULT_MARKET_CROP", mock_fail)
    
    res = get_market_price({})
    assert res["success"] == False
    assert res["market_price"] == "Unknown"
    assert res["price_trend"] == FALLBACK_PRICE_TREND
    assert res["confidence"] == 0.40
