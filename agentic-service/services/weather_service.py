from config import settings
from services.external_api_service import make_get_request
from utils.logger import setup_logger
from utils.fallback_messages import WEATHER_FALLBACK_MESSAGE

log = setup_logger("weather_service")

def get_current_weather(location: str = None) -> dict:
    """Fetch current weather from external API."""
    if not location:
        location = settings.DEFAULT_LOCATION
        
    if not settings.WEATHER_API_KEY:
        log.warning("WEATHER_API_KEY not set. Using fallback weather.")
        return get_fallback_weather(location)
        
    params = {
        "q": location,
        "appid": settings.WEATHER_API_KEY,
        "units": "metric"
    }
    
    data = make_get_request(settings.WEATHER_API_URL, params=params, timeout=settings.REQUEST_TIMEOUT_SECONDS)
    
    if data.get("success") is False or "weather" not in data:
        log.error(f"Weather API failed. Using fallback. Response: {data}")
        return get_fallback_weather(location)
        
    return normalize_weather_response(data, location)

def normalize_weather_response(raw_data: dict, location: str) -> dict:
    """Normalize OpenWeatherMap response."""
    try:
        temp = raw_data.get("main", {}).get("temp", "Unknown")
        condition = raw_data.get("weather", [{}])[0].get("main", "Unknown")
        humidity = raw_data.get("main", {}).get("humidity", "Unknown")
        wind_speed = raw_data.get("wind", {}).get("speed", "Unknown")
        
        advice = build_weather_advice({
            "temperature": temp,
            "condition": condition,
            "humidity": humidity
        })
        
        return {
            "location": raw_data.get("name", location),
            "temperature": f"{temp}C" if isinstance(temp, (int, float)) else temp,
            "condition": condition,
            "humidity": f"{humidity}%" if isinstance(humidity, (int, float)) else humidity,
            "wind_speed": f"{wind_speed} m/s" if isinstance(wind_speed, (int, float)) else wind_speed,
            "advice": advice
        }
    except Exception as e:
        log.error(f"Failed to normalize weather data: {e}")
        return get_fallback_weather(location)

def build_weather_advice(weather_data: dict) -> str:
    """Build basic agricultural advice based on weather conditions."""
    condition = str(weather_data.get("condition", "")).lower()
    temp = weather_data.get("temperature", 0)
    
    if "rain" in condition or "thunderstorm" in condition or "drizzle" in condition:
        return "Rain expected. Delay irrigation and pesticide application."
    elif isinstance(temp, (int, float)) and temp > 35:
        return "Hot weather expected. Irrigate crops early morning or evening."
    elif isinstance(temp, (int, float)) and temp < 10:
        return "Cold weather expected. Protect sensitive crops from frost."
    else:
        return "Weather conditions are stable."

def get_fallback_weather(location: str) -> dict:
    """Provide safe fallback weather data."""
    return {
        "location": location,
        "temperature": "Unknown",
        "condition": "Unknown",
        "humidity": "Unknown",
        "wind_speed": "Unknown",
        "advice": WEATHER_FALLBACK_MESSAGE
    }
