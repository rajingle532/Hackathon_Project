import pytest
from db.mongo import check_mongo_connection

def test_mongo_connection_failure(monkeypatch):
    monkeypatch.setattr("db.mongo.get_mongo_client", lambda: None)
    assert check_mongo_connection() == False

def test_mongo_connection_success(monkeypatch):
    class MockAdmin:
        def command(self, cmd): return True
    class MockClient:
        admin = MockAdmin()
    
    monkeypatch.setattr("db.mongo.get_mongo_client", lambda: MockClient())
    assert check_mongo_connection() == True
