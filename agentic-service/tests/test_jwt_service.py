import pytest
import time
from security.jwt_service import create_access_token, verify_access_token

def test_create_and_verify_jwt():
    payload = {"user_id": "123"}
    token = create_access_token(payload)
    assert token is not None
    
    verified = verify_access_token(token)
    assert verified is not None
    assert verified["user_id"] == "123"

def test_verify_invalid_jwt():
    assert verify_access_token("invalid.token.here") is None
