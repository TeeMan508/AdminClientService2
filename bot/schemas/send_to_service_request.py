from typing import Optional

from pydantic import BaseModel


class SendToServiceRequest(BaseModel):
    tg_id: str
    complaint: Optional[str] = None
    response: Optional[str] = None