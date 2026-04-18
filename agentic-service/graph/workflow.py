"""
LangGraph Workflow Definition (Module 2)
"""
from langgraph.graph import StateGraph, START, END
from graph.state import GraphState
from graph.router import classify_intent, route_intent
from agents.advisory_agent import advisory_agent_node
from agents.disease_agent import disease_agent_node
from agents.recommendation_agent import recommendation_agent_node
from agents.market_agent import market_agent_node
from agents.escalation_agent import escalation_agent_node
from utils.logger import setup_logger

log = setup_logger("workflow")

# ── Dummy Agents for Module 2 ────────────────────────────────────────

def create_dummy_agent(agent_name: str, intent: str):
    """Creates a dummy agent node for testing the router."""
    def dummy_node(state: GraphState) -> GraphState:
        log.info(f"Executing {agent_name}")
        reply = f"[{agent_name}] Placeholder response for intent '{intent}'. This module will be fully implemented in a future step."
        return {
            "agent_used": agent_name,
            "final_response": reply,
            "cards": [],
            "is_fallback": False,
            "context_used": {"dummy": True}
        }
    return dummy_node

# ── Graph Building ───────────────────────────────────────────────────

def build_graph():
    """Builds and returns the LangGraph application."""
    workflow = StateGraph(GraphState)
    
    # 1. Add intent classification node
    workflow.add_node("classify_intent", classify_intent)
    
    # 2. Add placeholder agent nodes
    agent_names = [
        "profile_update_agent", "video_support_agent"
    ]
    
    # Real agent node
    workflow.add_node("advisory_agent_node", advisory_agent_node)
    workflow.add_node("disease_agent_node", disease_agent_node)
    workflow.add_node("recommendation_agent_node", recommendation_agent_node)
    workflow.add_node("market_agent_node", market_agent_node)
    workflow.add_node("escalation_agent_node", escalation_agent_node)
    
    for agent in agent_names:
        intent_name = agent.replace("_agent", "")
        workflow.add_node(agent, create_dummy_agent(agent, intent_name))
        
    # Add an aggregator node that wraps it up before END
    def final_response_node(state: GraphState) -> GraphState:
        return state
        
    workflow.add_node("final_response", final_response_node)

    # 3. Define edges
    workflow.add_edge(START, "classify_intent")
    
    workflow.add_conditional_edges(
        "classify_intent",
        route_intent,
        {
            "advisory_agent": "advisory_agent_node",
            "weather_agent": "advisory_agent_node",
            "recommendation_agent": "recommendation_agent_node",
            "disease_agent": "disease_agent_node",
            "market_agent": "market_agent_node",
            "escalation_agent": "escalation_agent_node",
            "profile_update_agent": "profile_update_agent",
            "video_support_agent": "video_support_agent"
        }
    )
    
    workflow.add_edge("advisory_agent_node", "final_response")
    workflow.add_edge("disease_agent_node", "final_response")
    workflow.add_edge("recommendation_agent_node", "final_response")
    workflow.add_edge("market_agent_node", "final_response")
    workflow.add_edge("escalation_agent_node", "final_response")
    for agent in agent_names:
        workflow.add_edge(agent, "final_response")
        
    workflow.add_edge("final_response", END)
    
    app = workflow.compile()
    return app

# Singleton app
agent_app = build_graph()
