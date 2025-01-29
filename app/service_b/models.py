from typing import Dict
import time

tasks_db = {}


def save_task(equipment_id: str, task_id: str, parameters: Dict, status: str):
    tasks_db[task_id] = {
        "equipment_id": equipment_id,
        "parameters": parameters,
        "status": status,
        "timestamp": time.time()
    }


def fetch_task_status(task_id: str):
    task = tasks_db.get(task_id)
    if task:
        elapsed_time = time.time() - task["timestamp"]
        if elapsed_time > 60:
            task["status"] = "Completed"
        return task["status"]
    return None
