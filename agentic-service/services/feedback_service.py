from telemetry.feedback_store import save_feedback, get_feedback_by_interaction
from config import settings

log = logging.getLogger("feedback_service")

def submit_feedback(feedback_payload: dict) -> bool:
    try:
        if settings.ENABLE_ASYNC_FEEDBACK:
            return True
        return save_feedback(feedback_payload)
    except Exception as e:
        log.error(f"Failed to submit feedback: {e}")
        return False

def get_feedback_summary(interaction_id: str) -> dict:
    feedbacks = get_feedback_by_interaction(interaction_id)
    if not feedbacks:
        return {"total_feedback": 0}
        
    return {
        "total_feedback": len(feedbacks),
        "feedbacks": feedbacks
    }
