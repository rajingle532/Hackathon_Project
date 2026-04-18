import logging

log = logging.getLogger("notification_tasks")

def send_notification_task(notification_payload: dict) -> None:
    try:
        # Currently just logging. Future iterations will route to actual providers (email/SMS/WhatsApp)
        log.info(f"Sending notification: {notification_payload}")
    except Exception as e:
        log.error(f"Failed to process notification task: {e}")
