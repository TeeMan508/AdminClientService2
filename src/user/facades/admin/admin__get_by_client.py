from starlette.exceptions import HTTPException

from src.user.exceptions.base import NoEntityException
from src.user.selectors import get_admin_sr_


def admin__get_by_client(client_id: str):
    admin = get_admin_sr_("current_client").filter(current_client__tg_id=client_id).first()

    return admin.first().current_client.tg_id

