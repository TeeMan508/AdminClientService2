from celery.result import AsyncResult
from pydantic import BaseModel, Field
from starlette.responses import JSONResponse

from bot.api.tg.router import router

class TmpRequest(BaseModel):
    task_id: str

@router.post("/check_result")
async def check_result(data: TmpRequest):
    task_id = data.task_id
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result,
    }
    return JSONResponse(result)