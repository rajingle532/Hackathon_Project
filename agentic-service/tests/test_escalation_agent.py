import pytest
from agents.escalation_agent import escalation_agent_node

@pytest.mark.asyncio
async def test_escalation_agent_node_empty_state():
    state = {"messages": []}
    result = await escalation_agent_node(state)
    assert result == state

@pytest.mark.asyncio
async def test_escalation_agent_node_execution(monkeypatch):
    monkeypatch.setattr("agents.escalation_agent.translate_to_english", lambda msg, lang: msg)
    monkeypatch.setattr("agents.escalation_agent.translate_from_english", lambda msg, lang: msg)
    monkeypatch.setattr("agents.escalation_agent.needs_translation", lambda lang: False)
    monkeypatch.setattr("agents.escalation_agent.get_escalation_context", lambda intent, conf, msg: {
        "requires_escalation": True,
        "escalation_reason": "Testing",
        "consultant_type": "Agriculture Officer",
        "escalation_target": "Dept"
    })
    
    async def mock_generate(*args, **kwargs):
        return "Mock Escalation Response"
    monkeypatch.setattr("agents.escalation_agent.generate_escalation_response", mock_generate)
    
    class MockMessage:
        def __init__(self, content):
            self.content = content
            
    state = {
        "messages": [MockMessage("expert please")],
        "language": "English",
        "intent": "general",
        "metadata": {"agent_used": "disease_agent", "agent_confidence": 0.3},
        "context_used": {}
    }
    
    result = await escalation_agent_node(state)
    assert result["agent_used"] == "escalation_agent"
    assert result["final_answer"] == "Mock Escalation Response"
    assert result["metadata"]["requires_escalation"] == True
    assert result["metadata"]["consultant_type"] == "Agriculture Officer"
    assert "escalation_tool" in result["tools_used"]
    assert result["context_used"]["escalation"] == True
