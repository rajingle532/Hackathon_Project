import pytest
from background.task_manager import generate_task_id, schedule_task

def test_generate_task_id():
    task_id = generate_task_id("my_task")
    assert task_id.startswith("my_task_")
    assert len(task_id) > len("my_task_")

def test_schedule_task():
    class MockBackgroundTasks:
        def __init__(self):
            self.tasks = []
        def add_task(self, func, *args, **kwargs):
            self.tasks.append(func)
            
    bt = MockBackgroundTasks()
    tid = schedule_task(bt, "test", lambda x: x, 1)
    
    assert tid != ""
    assert len(bt.tasks) == 1
    
def test_schedule_task_none():
    tid = schedule_task(None, "test", lambda x: x, 1)
    assert tid == ""
