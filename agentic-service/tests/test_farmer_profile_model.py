import pytest
from models.farmer_profile_model import normalize_farmer_profile, validate_farmer_profile

def test_normalize_farmer_profile():
    profile = {"farmer_id": 123, "crops_grown": ["Wheat", 1]}
    norm = normalize_farmer_profile(profile)
    assert norm["farmer_id"] == "123"
    assert norm["crops_grown"] == ["Wheat", "1"]

def test_validate_farmer_profile():
    assert validate_farmer_profile({"farmer_id": "123"}) == True
    assert validate_farmer_profile({"location": "Punjab"}) == False
    assert validate_farmer_profile(None) == False
