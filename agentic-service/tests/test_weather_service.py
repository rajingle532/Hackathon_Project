import pytest
from services.weather_service import normalize_weather_response, build_weather_advice, get_fallback_weather

def test_normalize_weather_response():
    raw = {
        "weather": [{"main": "Clouds"}],
        "main": {"temp": 30.5, "humidity": 60},
        "wind": {"speed": 5.5},
        "name": "Delhi"
    }
    norm = normalize_weather_response(raw, "Delhi")
    assert norm["location"] == "Delhi"
    assert norm["temperature"] == "30.5C"
    assert norm["condition"] == "Clouds"
    assert norm["humidity"] == "60%"
    assert norm["wind_speed"] == "5.5 m/s"
    assert "stable" in norm["advice"].lower()

def test_build_weather_advice():
    advice_rain = build_weather_advice({"condition": "Rain", "temperature": 25})
    assert "delay irrigation" in advice_rain.lower()
    
    advice_hot = build_weather_advice({"condition": "Clear", "temperature": 40})
    assert "hot weather" in advice_hot.lower()

def test_get_fallback_weather():
    fallback = get_fallback_weather("Mumbai")
    assert fallback["location"] == "Mumbai"
    assert fallback["temperature"] == "Unknown"
    assert "Unable to fetch live weather" in fallback["advice"]
