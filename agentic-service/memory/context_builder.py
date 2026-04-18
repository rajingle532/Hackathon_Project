from services.conversation_history_service import format_history_for_prompt

def build_profile_context(profile: dict) -> str:
    if not profile:
        return ""
        
    lines = ["Farmer Profile:"]
    if profile.get("location"): lines.append(f"- Location: {profile['location']}")
    if profile.get("language"): lines.append(f"- Language: {profile['language']}")
    if profile.get("soil_type"): lines.append(f"- Soil Type: {profile['soil_type']}")
    if profile.get("irrigation_available") is True: lines.append("- Irrigation Available: Yes")
    
    crops = profile.get("crops_grown", [])
    if crops:
        lines.append(f"- Crops Grown: {', '.join(crops)}")
        
    if len(lines) == 1:
        return ""
        
    return "\n".join(lines)

def build_history_context(history: list[dict]) -> str:
    if not history:
        return ""
        
    formatted = format_history_for_prompt(history)
    return f"Recent Conversation History:\n{formatted}"

def build_memory_context(profile: dict, history: list[dict]) -> dict:
    return {
        "profile_context": build_profile_context(profile),
        "history_context": build_history_context(history)
    }
