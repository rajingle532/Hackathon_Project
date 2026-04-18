import pytest
from langchain_core.messages import HumanMessage
from agents.advisory_agent import advisory_agent_node
import asyncio

@pytest.mark.asyncio
async def test_advisory_agent_execution(monkeypatch):
    # Mock LLM call to return a fixed string
    async def mock_call_llm(prompt):
        return "Apply urea and water them tomorrow."
        
    monkeypatch.setattr("services.advisory_service.call_llm", mock_call_llm)
    
    state = {
        "messages": [HumanMessage(content="What should I do if wheat leaves are turning yellow? Will it rain?")],
        "language": "English"
    }
    
    new_state = await advisory_agent_node(state)
    
    assert new_state["agent_used"] == "advisory_agent"
    assert "weather_tool" in new_state["tools_used"]
    assert "retrieval_tool" in new_state["tools_used"]
    assert new_state["context_used"]["weather"] == True
    assert new_state["context_used"]["retrieval"] == True
    assert new_state["context_used"]["translation"] == False
    assert "Apply urea" in new_state["final_response"]

@pytest.mark.asyncio
async def test_advisory_agent_fallback(monkeypatch):
    async def mock_call_llm_fail(prompt):
        raise ValueError("API error")
        
    monkeypatch.setattr("services.advisory_service.call_llm", mock_call_llm_fail)
    
    state = {
        "messages": [HumanMessage(content="Help me")],
        "language": "English"
    }
    
    new_state = await advisory_agent_node(state)
    assert new_state["is_fallback"] == True
    assert "unable to generate" in new_state["final_response"]
