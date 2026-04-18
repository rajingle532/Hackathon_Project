import pytest
from tools.market_tool import market_needed, get_market_context

def test_market_needed():
    assert market_needed("what is the price") == True
    assert market_needed("should I sell") == True
    assert market_needed("weather today") == False

def test_get_market_context(monkeypatch):
    def mock_get(profile):
        return {"market_price": "₹100", "price_trend": "up", "confidence": 0.8}
        
    monkeypatch.setattr("tools.market_tool.get_market_price", mock_get)
    
    ctx = get_market_context("wheat price")
    assert ctx["market_price"] == "₹100"
    assert ctx["price_trend"] == "up"
    assert ctx["market_profile"]["commodity_name"] == "Wheat"
