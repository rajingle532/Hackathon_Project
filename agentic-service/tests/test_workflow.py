"""
Test Module 2: LangGraph Workflow
"""
import pytest
from graph.state import GraphState
from graph.workflow import agent_app
from langchain_core.messages import HumanMessage

def test_workflow_dummy_execution():
    """Test that the workflow routes a basic message."""
    
    initial_state = {
        "farmer_id": "test_123",
        "language": "English",
        "messages": [HumanMessage(content="Hello")],
        "intent": None,
        "agent_used": None,
        "final_response": None,
        "cards": [],
        "is_fallback": False,
        "context_used": {}
    }
    
    # We invoke the graph. If LLM is configured, it will classify, otherwise fallback to 'unknown' -> advisory_agent.
    try:
        final_state = agent_app.invoke(initial_state)
        
        assert final_state.get("intent") is not None
        assert final_state.get("agent_used") is not None
        assert final_state.get("final_response") is not None
        
        # In fallback or any case, we should get some response back from a dummy agent
        assert "Placeholder response" in final_state.get("final_response")
    except Exception as e:
        pytest.fail(f"Graph execution failed: {e}")
