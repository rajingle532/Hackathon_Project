import pytest
from agents.market_agent import market_agent_node

@pytest.mark.asyncio
async def test_market_agent_node_empty_state():
    state = {"messages": []}
    result = await market_agent_node(state)
    assert result == state

@pytest.mark.asyncio
async def test_market_agent_node_execution(monkeypatch):
    monkeypatch.setattr("agents.market_agent.translate_to_english", lambda msg, lang: msg)
    monkeypatch.setattr("agents.market_agent.translate_from_english", lambda msg, lang: msg)
    monkeypatch.setattr("agents.market_agent.needs_translation", lambda lang: False)
    monkeypatch.setattr("agents.market_agent.get_market_context", lambda msg: {
        "commodity_name": "Wheat",
        "market_location": "Delhi",
        "market_price": "₹100",
        "price_trend": "up",
        "confidence": 0.8
    })
    monkeypatch.setattr("agents.market_agent.retrieve_context_with_metadata", lambda msg: {"retrieval_context": "Rag", "sources": ["mock.txt"]})
    
    async def mock_generate(*args, **kwargs):
        return "Mock LLM Response"
    monkeypatch.setattr("agents.market_agent.generate_market_response", mock_generate)
    
    class MockMessage:
        def __init__(self, content):
            self.content = content
            
    state = {
        "messages": [MockMessage("wheat price")],
        "language": "English",
        "metadata": {},
        "context_used": {}
    }
    
    result = await market_agent_node(state)
    assert result["agent_used"] == "market_agent"
    assert result["final_answer"] == "Mock LLM Response"
    assert result["metadata"]["commodity_name"] == "Wheat"
    assert "market_tool" in result["tools_used"]
    assert result["context_used"]["market"] == True
