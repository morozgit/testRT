from fastapi import APIRouter, HTTPException
import asyncio
import random
from pydantic import BaseModel
from typing import List, Optional


class Parameters(BaseModel):
    username: str
    password: str
    vlan: Optional[int] = None
    interfaces: List[int]


server_a = APIRouter(
    prefix="/api/v1",
)


def some_external_service_call():
    if random.choice([False, False]):
        raise Exception("External service failed")


@server_a.post("/equipment/cpe/{id}")
async def configure_equipment(
    id: str,
    timeoutInSeconds: int,
    parameters: Parameters
):
    if not id.isalnum() or len(id) < 6:
        raise HTTPException(status_code=404, detail="The requested equipment is not found")

    await asyncio.sleep(min(timeoutInSeconds, 60))

    try:
        some_external_service_call()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal provisioning exception: {str(e)}")

    return {"code": 200, "message": "success"}
