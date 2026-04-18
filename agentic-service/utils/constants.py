"""
Agentic Service — Shared Constants
====================================
"""

# ── Intent categories (used by LangGraph router in Module 2) ─────────
INTENTS = [
    "advisory",
    "weather",
    "recommendation",
    "disease",
    "market",
    "escalation",
    "profile_update",
    "video_support",
    "greeting",
    "unknown",
]

# ── Agent names ──────────────────────────────────────────────────────
AGENT_ADVISORY = "advisory_agent"
AGENT_DISEASE = "disease_agent"
AGENT_RECOMMENDATION = "recommendation_agent"
AGENT_MARKET = "market_agent"
AGENT_ESCALATION = "escalation_agent"
AGENT_PROFILE = "profile_agent"
AGENT_VIDEO = "video_agent"

# ── HTTP headers ─────────────────────────────────────────────────────
JSON_HEADERS = {"Content-Type": "application/json"}
