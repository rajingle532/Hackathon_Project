import uuid
import logging
from fastapi import BackgroundTasks

log = logging.getLogger("task_manager")

def generate_task_id(task_name: str) -> str:
    return f"{task_name}_{uuid.uuid4().hex[:8]}"

def schedule_task(
    background_tasks: BackgroundTasks,
    task_name: str,
    task_callable,
    *args,
    **kwargs
) -> str:
    try:
        task_id = generate_task_id(task_name)
        if background_tasks is not None:
            background_tasks.add_task(task_callable, *args, **kwargs)
            log.info(f"Scheduled task {task_name} with ID {task_id}")
            return task_id
        else:
            log.warning(f"Failed to schedule task {task_name}: no BackgroundTasks provided")
            return ""
    except Exception as e:
        log.error(f"Error scheduling task {task_name}: {e}")
        return ""
