from starlette.exceptions import HTTPException

from src.user.exceptions.base import BusyAdminException
from src.user.facades.client import client__get_unhandled
from src.user.interactors import set_client_to_admin
from src.user.logger import logger
from src.user.selectors import get_admin_, get_client_


def admin__set_next_client(admin_id: str) -> str:
    admin = get_admin_(tg_id=admin_id)
    client = client__get_unhandled()

    if admin.is_busy:
        raise BusyAdminException("Admin is busy")

    set_client_to_admin(client, admin)

    return client.complaint



