from unittest.mock import patch, MagicMock
from hindsight.hindsight_service import save_hindsight, fetch_hindsight

@patch('hindsight.hindsight_config.hindsight_config.enabled', True)
@patch('hindsight.hindsight_service.create_hindsight_log')
def test_save_hindsight_success(mock_create):
    mock_create.return_value = {"status": "success"}
    
    result = save_hindsight({
        "interaction_id": "test_id",
        "farmer_id": "farmer_1",
        "agent_used": "disease_agent"
    })
    
    assert result == True
    mock_create.assert_called_once()
    
    # Verify the mapper converted keys
    called_payload = mock_create.call_args[0][0]
    assert "event_id" in called_payload
    assert called_payload["event_id"] == "test_id"

@patch('hindsight.hindsight_config.hindsight_config.enabled', True)
@patch('hindsight.hindsight_service.create_hindsight_log')
def test_save_hindsight_failure(mock_create):
    mock_create.return_value = {"status": "error", "message": "Failed"}
    
    result = save_hindsight({"interaction_id": "test_id"})
    assert result == False

@patch('hindsight.hindsight_config.hindsight_config.enabled', True)
@patch('hindsight.hindsight_service.get_hindsight_logs')
def test_fetch_hindsight_success(mock_get):
    mock_get.return_value = [{"event_id": "test_id", "user_id": "farmer_1"}]
    
    result = fetch_hindsight("test_id")
    
    assert len(result) == 1
    assert result[0]["interaction_id"] == "test_id"
    assert result[0]["farmer_id"] == "farmer_1"

@patch('hindsight.hindsight_config.hindsight_config.enabled', True)
@patch('hindsight.hindsight_service.get_hindsight_logs')
def test_fetch_hindsight_failure(mock_get):
    mock_get.return_value = []
    
    result = fetch_hindsight("test_id")
    assert result == []
