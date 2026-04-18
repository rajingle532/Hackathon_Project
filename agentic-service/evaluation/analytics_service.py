def summarize_telemetry(telemetry_events: list[dict]) -> dict:
    if not telemetry_events:
        return {}
        
    total = len(telemetry_events)
    total_score = 0.0
    fallbacks = 0
    agents = {}
    
    for event in telemetry_events:
        total_score += event.get("response_score", 0.0)
        if event.get("is_fallback"):
            fallbacks += 1
            
        agent = event.get("agent_used", "none")
        if agent not in agents:
            agents[agent] = {"count": 0, "total_score": 0.0, "fallbacks": 0}
        agents[agent]["count"] += 1
        agents[agent]["total_score"] += event.get("response_score", 0.0)
        if event.get("is_fallback"):
            agents[agent]["fallbacks"] += 1
            
    # Compute averages
    for agent, data in agents.items():
        data["average_score"] = data["total_score"] / data["count"] if data["count"] > 0 else 0.0
        
    return {
        "total_events": total,
        "average_response_score": total_score / total if total > 0 else 0.0,
        "fallback_frequency": fallbacks / total if total > 0 else 0.0,
        "agent_breakdown": agents
    }

def summarize_feedback(feedback_logs: list[dict]) -> dict:
    if not feedback_logs:
        return {}
        
    total = len(feedback_logs)
    thumbs_up = sum(1 for f in feedback_logs if f.get("feedback_type") == "thumbs_up")
    thumbs_down = sum(1 for f in feedback_logs if f.get("feedback_type") == "thumbs_down")
    
    return {
        "total_feedback": total,
        "thumbs_up": thumbs_up,
        "thumbs_down": thumbs_down,
        "approval_ratio": thumbs_up / total if total > 0 else 0.0
    }

def summarize_hindsight(hindsight_logs: list[dict]) -> dict:
    if not hindsight_logs:
        return {}
        
    total = len(hindsight_logs)
    successful = sum(1 for h in hindsight_logs if h.get("outcome_status") == "successful")
    failed = sum(1 for h in hindsight_logs if h.get("outcome_status") == "failed")
    
    return {
        "total_logs": total,
        "successful_outcomes": successful,
        "failed_outcomes": failed,
        "success_ratio": successful / total if total > 0 else 0.0
    }
