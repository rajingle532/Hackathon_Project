import pytest
from tools.farm_profile_parser_tool import extract_soil_type, extract_season, extract_rainfall_level, extract_irrigation_availability, extract_location, build_farm_profile

def test_extract_soil_type():
    assert extract_soil_type("I have loamy soil") == "loamy"
    assert extract_soil_type("black soil here") == "black"
    assert extract_soil_type("unknown") == "loamy" # default

def test_extract_season():
    assert extract_season("monsoon season") == "kharif"
    assert extract_season("winter planting") == "rabi"
    assert extract_season("spring") == "kharif" # default

def test_extract_rainfall_level():
    assert extract_rainfall_level("heavy rain") == "high"
    assert extract_rainfall_level("dry") == "low"
    assert extract_rainfall_level("nothing") == "medium" # default

def test_extract_irrigation_availability():
    assert extract_irrigation_availability("I have a borewell") == True
    assert extract_irrigation_availability("no water") == False

def test_extract_location():
    assert extract_location("I am from punjab") == "Punjab"
    assert extract_location("nowhere") == "Delhi" # default

def test_build_farm_profile():
    msg = "I am from punjab, have black soil, during winter, with low rainfall and a tube well"
    profile = build_farm_profile(msg)
    assert profile["soil_type"] == "black"
    assert profile["season"] == "rabi"
    assert profile["location"] == "Punjab"
    assert profile["rainfall_level"] == "low"
    assert profile["irrigation_available"] == True
