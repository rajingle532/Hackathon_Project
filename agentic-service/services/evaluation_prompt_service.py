def build_agent_summary_prompt(agent_name: str, analytics: dict) -> str:
    """Generate reusable evaluation summaries for future dashboards."""
    if not analytics:
        return f"No analytics available for {agent_name}."
        
    prompt = f"=== ANALYTICS SUMMARY FOR {agent_name.upper()} ===\n"
    prompt += f"Total Events: {analytics.get('total_events', 0)}\n"
    prompt += f"Average Score: {analytics.get('average_response_score', 0.0):.2f}\n"
    
    return prompt
