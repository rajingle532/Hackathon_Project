import pytest
from services.conversation_history_service import format_history_for_prompt, filter_relevant_history

def test_format_history_for_prompt():
    history = [
        {"role": "user", "content": "hi"},
        {"role": "system", "content": "hello"}
    ]
    formatted = format_history_for_prompt(history)
    assert "User: hi" in formatted
    assert "System: hello" in formatted
    
def test_filter_relevant_history():
    history = [{"role": "user", "content": "hi"}]
    filtered = filter_relevant_history(history, "general")
    assert len(filtered) == 1
