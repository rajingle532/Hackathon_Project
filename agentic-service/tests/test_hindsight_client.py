from unittest.mock import patch, MagicMock
from hindsight.hindsight_client import create_hindsight_log, get_hindsight_logs, check_hindsight_connection
from hindsight.hindsight_config import hindsight_config
import requests

@patch('hindsight.hindsight_config.hindsight_config.base_url', 'http://mock-api.com')
@patch('hindsight.hindsight_config.hindsight_config.api_key', 'mock_key')
@patch('requests.post')
def test_create_hindsight_log_success(mock_post):
    mock_response = MagicMock()
    mock_response.json.return_value = {"status": "success", "id": "123"}
    mock_response.raise_for_status.return_value = None
    mock_post.return_value = mock_response

    result = create_hindsight_log({"event_id": "test"})
    
    assert result["status"] == "success"
    mock_post.assert_called_once()
    args, kwargs = mock_post.call_args
    assert kwargs["headers"]["Authorization"] == "Bearer mock_key"

@patch('hindsight.hindsight_config.hindsight_config.base_url', 'http://mock-api.com')
@patch('requests.post')
def test_create_hindsight_log_auth_failure(mock_post):
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("401 Client Error: Unauthorized")
    mock_post.return_value = mock_response

    result = create_hindsight_log({"event_id": "test"})
    
    assert result["status"] == "error"
    assert "401" in result["message"]

@patch('hindsight.hindsight_config.hindsight_config.base_url', 'http://mock-api.com')
@patch('requests.post')
def test_create_hindsight_log_timeout(mock_post):
    mock_post.side_effect = requests.exceptions.Timeout("Connection timed out")

    result = create_hindsight_log({"event_id": "test"})
    
    assert result["status"] == "error"
    assert "Connection timed out" in result["message"]

@patch('hindsight.hindsight_config.hindsight_config.base_url', 'http://mock-api.com')
@patch('requests.get')
def test_check_hindsight_connection(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    assert check_hindsight_connection() == True

@patch('hindsight.hindsight_config.hindsight_config.base_url', '')
def test_fallback_behavior_unconfigured():
    # When not configured, it should fail gracefully
    result = create_hindsight_log({"event_id": "test"})
    assert result["status"] == "fallback"
