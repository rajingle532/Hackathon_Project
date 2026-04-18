import pytest
from services.consultant_service import get_consultant_details

def test_get_consultant_details():
    res1 = get_consultant_details("Plant Pathologist")
    assert "university" in res1["contact_recommendation"].lower()
    
    res2 = get_consultant_details("Market Advisor")
    assert "mandi" in res2["contact_recommendation"].lower()
    
    res3 = get_consultant_details("Agriculture Officer")
    assert "agriculture officer" in res3["contact_recommendation"].lower()
