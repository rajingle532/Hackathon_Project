from typing import List, Dict
import datetime

# Mock DB for conversations
_MOCK_HISTORY = {}

def get_recent_conversation_history(farmer_id: str, limit: int = 10) -> list[dict]:
    history = _MOCK_HISTORY.get(farmer_id, [])
    return history[-limit:]

def save_conversation_message(farmer_id: str, role: str, content: str, metadata: dict = None) -> None:
    if farmer_id not in _MOCK_HISTORY:
        _MOCK_HISTORY[farmer_id] = []
        
    msg = {
        "role": role,
        "content": content,
        "timestamp": datetime.datetime.now().isoformat()
    }
    if metadata:
        msg["metadata"] = metadata
        
    _MOCK_HISTORY[farmer_id].append(msg)

def save_agent_interaction(farmer_id: str, intent: str, response: dict) -> None:
    if farmer_id not in _MOCK_HISTORY:
        _MOCK_HISTORY[farmer_id] = []
        
    _MOCK_HISTORY[farmer_id].append({
        "role": "system",
        "intent": intent,
        "content": response.get("reply", ""),
        "metadata": response.get("metadata", {}),
        "timestamp": datetime.datetime.now().isoformat()
    })
