from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import uuid

from .tasks import add_task_to_queue
from .models import save_task, fetch_task_status


class ConfigRequest(BaseModel):
    timeoutInSeconds: int
    parameters: dict


server_b = APIRouter(
    prefix="/api/v1",
)


@server_b.post("/equipment/cpe/{id}")
async def create_task(id: str, config: ConfigRequest):
    task_id = str(uuid.uuid4())

    save_task(id, task_id, config.dict(), "queued")

    add_task_to_queue(task_id, id, config.dict())

    return {"code": 200, "taskId": task_id}


@server_b.get("/equipment/cpe/{id}/task/{task}")
async def get_task_status(id: str, task: str):
    task_status = fetch_task_status(task)

    if task_status is None:
        raise HTTPException(status_code=404, detail="The requested task is not found")

    return {"code": 200, "message": task_status}