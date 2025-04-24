from typing import Optional

from pydantic import BaseModel

class AdminCredentials(BaseModel):
    tg_id: str
    response: Optional[str] = None