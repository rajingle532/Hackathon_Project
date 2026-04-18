import pytest
from tools.commodity_parser_tool import extract_commodity, extract_market_location, detect_selling_intent, build_market_profile
import config

def test_extract_commodity():
    assert extract_commodity("what is the price of gehun") == "Wheat"
    assert extract_commodity("soyabean rate") == "Soybean"
    assert extract_commodity("unknown") == config.settings.DEFAULT_MARKET_CROP

def test_extract_market_location():
    assert extract_market_location("in punjab") == "Punjab"
    assert extract_market_location("nowhere") == config.settings.DEFAULT_MARKET_LOCATION

def test_detect_selling_intent():
    assert detect_selling_intent("should I sell now") == True
    assert detect_selling_intent("mandi rate") == True
    assert detect_selling_intent("hello") == False

def test_build_market_profile():
    msg = "should I sell my rice in haryana"
    profile = build_market_profile(msg)
    assert profile["commodity_name"] == "Rice"
    assert profile["market_location"] == "Haryana"
    assert profile["selling_intent"] == True
