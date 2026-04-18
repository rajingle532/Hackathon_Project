import datetime

def build_event_payload(
    event_type: str,
    farmer_id: str,
    interaction_id: str,
    metadata: dict
) -> dict:
    return {
        "event_type": event_type,
        "farmer_id": farmer_id,
        "interaction_id": interaction_id,
        "metadata": metadata,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }
