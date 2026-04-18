import pytest
from services.market_prompt_service import build_market_prompt

def test_build_market_prompt():
    ctx = {
        "commodity_name": "Wheat",
        "market_location": "Delhi",
        "market_price": "₹100",
        "price_trend": "up",
        "confidence": 0.8,
        "selling_advice": "Sell"
    }
    prompt = build_market_prompt("price?", ctx, "RAG")
    assert "price?" in prompt
    assert "Wheat" in prompt
    assert "₹100" in prompt
    assert "RAG" in prompt
    assert "WARNING" not in prompt

def test_build_market_prompt_warning():
    ctx = {"confidence": 0.4}
    prompt = build_market_prompt("price?", ctx, "")
    assert "WARNING:" in prompt
