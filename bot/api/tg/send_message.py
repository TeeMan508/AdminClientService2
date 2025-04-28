from typing import Optional

from starlette.requests import Request
from starlette.responses import JSONResponse

from bot.bot import bot

from .router import router
from ...logger import logger, correlation_id_ctx
from ...metrics import TOTAL_REQ
from ...schemas.send_msg_request import SendMessageRequest
from fastapi import status, Header


@router.post('/send_message')
async def send_message(request: SendMessageRequest, x_correlation_id: Optional[str] = Header(None)):
    TOTAL_REQ.inc()
    correlation_id_ctx.set(x_correlation_id)

    logger.info("Sending message to user")
    await bot.send_message(int(request.tg_id), request.msg)

    return JSONResponse({}, status_code=status.HTTP_200_OK)