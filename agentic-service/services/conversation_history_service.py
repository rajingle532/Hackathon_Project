def format_history_for_prompt(history: list[dict], max_messages: int = 5) -> str:
    if not history:
        return "No recent conversation history."
        
    formatted = []
    # Take the last N messages
    recent = history[-max_messages:]
    for msg in recent:
        role = "User" if msg.get("role") == "user" else "System"
        content = msg.get("content", "")
        formatted.append(f"{role}: {content}")
        
    return "\n".join(formatted)

def filter_relevant_history(history: list[dict], intent: str) -> list[dict]:
    # In a simple heuristic, just return the whole history.
    # A more advanced version would semantically filter.
    return history
