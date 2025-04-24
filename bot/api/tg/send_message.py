from starlette.requests import Request
from starlette.responses import JSONResponse

from bot.bot import bot
from .router import router
from ...logger import logger
from ...schemas.send_msg_request import SendMessageRequest
from fastapi import status


@router.post('/send_message')
async def send_message(request: SendMessageRequest):
    await bot.send_message(int(request.tg_id), request.msg)
    return JSONResponse({}, status_code=status.HTTP_200_OK)