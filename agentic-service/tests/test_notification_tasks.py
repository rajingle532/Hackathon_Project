import pytest
from background.notification_tasks import send_notification_task

def test_send_notification_task():
    # Mostly checking that it doesn't crash since it's just logging
    send_notification_task({"event_type": "test"})
