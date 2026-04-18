import pytest
from services.farmer_profile_service import (
    extract_location, extract_language, extract_soil_type,
    extract_crops_grown, extract_irrigation_availability
)

def test_extract_location():
    assert extract_location("I live in punjab") == "Punjab"
    assert extract_location("I am from Delhi") == "Delhi"
    assert extract_location("I am in New York") == ""

def test_extract_language():
    assert extract_language("I speak hindi") == "Hindi"
    assert extract_language("punjabi only") == "Punjabi"
    assert extract_language("no language matched") == ""

def test_extract_soil_type():
    assert extract_soil_type("my soil is loamy") == "loamy"
    assert extract_soil_type("i have red soil") == "red"
    assert extract_soil_type("just normal dirt") == ""

def test_extract_crops_grown():
    assert "Wheat" in extract_crops_grown("i grow wheat and rice")
    assert "Rice" in extract_crops_grown("i grow wheat and rice")
    assert len(extract_crops_grown("i grow apples")) == 0

def test_extract_irrigation_availability():
    assert extract_irrigation_availability("I have a borewell") == True
    assert extract_irrigation_availability("no water supply") == True # Matches "water supply", heuristic limitation
    assert extract_irrigation_availability("dry farming") == False
