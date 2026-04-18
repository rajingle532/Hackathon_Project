import pytest
from unittest.mock import patch, MagicMock
from hindsight.hindsight_retry import execute_with_retry

@patch('hindsight.hindsight_config.hindsight_config.max_retries', 3)
@patch('time.sleep') # mock sleep to keep tests fast
def test_execute_with_retry_success_first_try(mock_sleep):
    mock_task = MagicMock(return_value="success")
    
    result = execute_with_retry(mock_task)
    
    assert result == "success"
    mock_task.assert_called_once()
    mock_sleep.assert_not_called()

@patch('hindsight.hindsight_config.hindsight_config.max_retries', 3)
@patch('time.sleep')
def test_execute_with_retry_success_after_retries(mock_sleep):
    mock_task = MagicMock(side_effect=[Exception("Fail 1"), Exception("Fail 2"), "success"])
    
    result = execute_with_retry(mock_task)
    
    assert result == "success"
    assert mock_task.call_count == 3
    assert mock_sleep.call_count == 2

@patch('hindsight.hindsight_config.hindsight_config.max_retries', 3)
@patch('time.sleep')
def test_execute_with_retry_failure(mock_sleep):
    mock_task = MagicMock(side_effect=[Exception("Fail 1"), Exception("Fail 2"), Exception("Fail 3")])
    
    result = execute_with_retry(mock_task)
    
    assert result is None
    assert mock_task.call_count == 3
    assert mock_sleep.call_count == 2
