import pytest
from memory.farmer_profile_store import get_farmer_profile, update_farmer_profile, merge_farmer_profile

def test_merge_farmer_profile():
    existing = {"farmer_id": "1", "location": "Punjab", "crops_grown": ["Wheat"]}
    incoming = {"location": "Haryana", "crops_grown": ["Rice"], "soil_type": "loamy"}
    merged = merge_farmer_profile(existing, incoming)
    
    assert merged["farmer_id"] == "1"
    assert merged["location"] == "Haryana"
    assert "Wheat" in merged["crops_grown"]
    assert "Rice" in merged["crops_grown"]
    assert merged["soil_type"] == "loamy"
    assert "last_updated" in merged

def test_get_and_update_farmer_profile():
    profile = get_farmer_profile("test_1")
    assert profile["farmer_id"] == "test_1"
    
    updated = update_farmer_profile("test_1", {"location": "Delhi"})
    assert updated["location"] == "Delhi"
    
    profile_again = get_farmer_profile("test_1")
    assert profile_again["location"] == "Delhi"
