from pydantic import BaseModel


class SendMessageRequest(BaseModel):
    tg_id: str
    msg: str
