from starlette.exceptions import HTTPException

from src.user.exceptions.base import NoEntityException
from src.user.selectors import get_admin_sr_

def admin__get_current_client(admin_id: str) -> str:
    admin = get_admin_sr_("current_client", tg_id=admin_id).first()

    if not admin.current_client:
        raise NoEntityException("No current client found for admin")

    return admin.current_client.tg_id

