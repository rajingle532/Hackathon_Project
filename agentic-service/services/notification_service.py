def build_notification_payload(
    event_type: str,
    farmer_id: str,
    message: str,
    metadata: dict
) -> dict:
    return {
        "event_type": event_type,
        "farmer_id": farmer_id,
        "message": message,
        "metadata": metadata
    }
