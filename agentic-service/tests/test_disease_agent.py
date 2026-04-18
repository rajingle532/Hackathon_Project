import pytest
from agents.disease_agent import disease_agent_node

@pytest.mark.asyncio
async def test_disease_agent_node_empty_state():
    state = {"messages": []}
    result = await disease_agent_node(state)
    assert result == state

@pytest.mark.asyncio
async def test_disease_agent_node_execution(monkeypatch):
    # Mock all dependencies
    monkeypatch.setattr("agents.disease_agent.translate_to_english", lambda msg, lang: msg)
    monkeypatch.setattr("agents.disease_agent.translate_from_english", lambda msg, lang: msg)
    monkeypatch.setattr("agents.disease_agent.needs_translation", lambda lang: False)
    monkeypatch.setattr("agents.disease_agent.get_disease_context", lambda msg, path: {"disease_name": "Mock Disease", "confidence": 0.9, "symptoms_detected": []})
    monkeypatch.setattr("agents.disease_agent.retrieve_context_with_metadata", lambda msg: {"retrieval_context": "Mock Rag", "sources": ["mock.txt"]})
    
    async def mock_generate(*args, **kwargs):
        return "Mock LLM Response"
    monkeypatch.setattr("agents.disease_agent.generate_disease_response", mock_generate)
    
    class MockMessage:
        def __init__(self, content):
            self.content = content
            
    state = {
        "messages": [MockMessage("fungus on leaves")],
        "language": "English",
        "metadata": {},
        "context_used": {}
    }
    
    result = await disease_agent_node(state)
    assert result["agent_used"] == "disease_agent"
    assert result["final_answer"] == "Mock LLM Response"
    assert result["metadata"]["disease_name"] == "Mock Disease"
    assert "disease_tool" in result["tools_used"]
    assert result["context_used"]["disease"] == True
