import pytest
from tools.weather_tool import weather_needed, get_weather_context, extract_location_from_message

def test_weather_needed():
    assert weather_needed("Will it rain tomorrow?") == True
    assert weather_needed("Should I irrigate my crops?") == True
    assert weather_needed("What is the temperature?") == True
    assert weather_needed("My wheat leaves are yellow.") == False

def test_extract_location_from_message():
    assert extract_location_from_message("Will it rain in Delhi?") == "Delhi"
    assert extract_location_from_message("Weather in Punjab") == "Punjab"
    assert extract_location_from_message("How is the weather") == "Delhi" # Default

def test_get_weather_context(monkeypatch):
    # Mock the get_current_weather to avoid API calls during test
    def mock_get_current_weather(location):
        return {"location": location, "temperature": "30C", "condition": "Sunny"}
    
    monkeypatch.setattr("tools.weather_tool.get_current_weather", mock_get_current_weather)
    
    ctx = get_weather_context("rain in Mumbai")
    assert "temperature" in ctx
    assert ctx["location"] == "Mumbai"
    
    ctx2 = get_weather_context("hello")
    assert ctx2 == {}
