import pytest
from agents.recommendation_agent import recommendation_agent_node

@pytest.mark.asyncio
async def test_recommendation_agent_node_empty_state():
    state = {"messages": []}
    result = await recommendation_agent_node(state)
    assert result == state

@pytest.mark.asyncio
async def test_recommendation_agent_node_execution(monkeypatch):
    monkeypatch.setattr("agents.recommendation_agent.translate_to_english", lambda msg, lang: msg)
    monkeypatch.setattr("agents.recommendation_agent.translate_from_english", lambda msg, lang: msg)
    monkeypatch.setattr("agents.recommendation_agent.needs_translation", lambda lang: False)
    monkeypatch.setattr("agents.recommendation_agent.get_recommendation_context", lambda msg: {
        "recommended_crops": ["Rice"],
        "confidence": 0.8,
        "farm_profile": {"soil_type": "loamy"}
    })
    monkeypatch.setattr("agents.recommendation_agent.retrieve_context_with_metadata", lambda msg: {"retrieval_context": "Rag", "sources": ["mock.txt"]})
    
    async def mock_generate(*args, **kwargs):
        return "Mock LLM Response"
    monkeypatch.setattr("agents.recommendation_agent.generate_recommendation_response", mock_generate)
    
    class MockMessage:
        def __init__(self, content):
            self.content = content
            
    state = {
        "messages": [MockMessage("What crop should I grow?")],
        "language": "English",
        "metadata": {},
        "context_used": {}
    }
    
    result = await recommendation_agent_node(state)
    assert result["agent_used"] == "recommendation_agent"
    assert result["final_answer"] == "Mock LLM Response"
    assert result["metadata"]["recommended_crops"] == ["Rice"]
    assert "recommendation_tool" in result["tools_used"]
    assert result["context_used"]["recommendation"] == True
