import pytest
from services.external_api_service import make_get_request
import requests

def test_make_get_request_success(monkeypatch):
    class MockResponse:
        def json(self):
            return {"data": "ok", "success": True}
        def raise_for_status(self):
            pass
            
    def mock_get(*args, **kwargs):
        return MockResponse()
        
    monkeypatch.setattr(requests, "get", mock_get)
    result = make_get_request("http://fake.url")
    assert result["data"] == "ok"

def test_make_get_request_timeout(monkeypatch):
    def mock_get(*args, **kwargs):
        raise requests.exceptions.Timeout("Timeout")
        
    monkeypatch.setattr(requests, "get", mock_get)
    result = make_get_request("http://fake.url")
    assert result["success"] == False
    assert "timeout" in result["error"].lower()
