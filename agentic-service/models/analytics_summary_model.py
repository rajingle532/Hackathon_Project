def normalize_analytics_summary(summary: dict) -> dict:
    if not isinstance(summary, dict):
        return {}
    return {
        "telemetry_summary": summary.get("telemetry_summary", {}),
        "feedback_summary": summary.get("feedback_summary", {}),
        "hindsight_summary": summary.get("hindsight_summary", {})
    }

def validate_analytics_summary(summary: dict) -> bool:
    if not isinstance(summary, dict):
        return False
    return True
