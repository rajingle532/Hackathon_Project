import pytest
import time
from security.rate_limit_service import check_rate_limit, increment_rate_limit
from config import settings

def test_rate_limit(monkeypatch):
    monkeypatch.setattr(settings, "ENABLE_RATE_LIMITING", True)
    monkeypatch.setattr(settings, "RATE_LIMIT_REQUESTS", 2)
    monkeypatch.setattr(settings, "RATE_LIMIT_WINDOW_SECONDS", 10)
    
    # Reset internal state
    from security import rate_limit_service
    rate_limit_service._rate_limits = {}
    
    identifier = "127.0.0.1"
    
    assert check_rate_limit(identifier) is True
    increment_rate_limit(identifier)
    assert check_rate_limit(identifier) is True
    increment_rate_limit(identifier)
    
    assert check_rate_limit(identifier) is False
