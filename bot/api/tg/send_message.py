from pydantic import BaseModel

from bot.bot import bot
from .router import router

class MessageModelRequest(BaseModel):
    msg: str
    client_id: int

@router.post('/send_message')
async def send_message(request: MessageModelRequest):
    await bot.send_message(request.client_id, request.msg)