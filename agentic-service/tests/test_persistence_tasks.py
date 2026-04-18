import pytest
from background.persistence_tasks import _retry_wrapper

def test_retry_wrapper_success():
    calls = []
    def mock_func():
        calls.append(1)
        return True
        
    res = _retry_wrapper(mock_func)
    assert res == True
    assert len(calls) == 1

def test_retry_wrapper_failure(monkeypatch):
    monkeypatch.setattr("background.persistence_tasks.time.sleep", lambda x: None)
    
    calls = []
    def mock_func():
        calls.append(1)
        raise Exception("failed")
        
    res = _retry_wrapper(mock_func)
    assert res == False
    assert len(calls) == 3 # Default max retries
