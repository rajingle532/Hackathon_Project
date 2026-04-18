import pytest
from memory.conversation_store import get_recent_conversation_history, save_conversation_message, save_agent_interaction

def test_save_and_get_conversation():
    save_conversation_message("farmer_1", "user", "test message")
    history = get_recent_conversation_history("farmer_1")
    assert len(history) >= 1
    assert history[-1]["content"] == "test message"
    assert history[-1]["role"] == "user"

def test_save_agent_interaction():
    save_agent_interaction("farmer_1", "disease", {"reply": "you have a disease", "metadata": {"confidence": 0.9}})
    history = get_recent_conversation_history("farmer_1")
    assert history[-1]["role"] == "system"
    assert history[-1]["content"] == "you have a disease"
    assert history[-1]["intent"] == "disease"
