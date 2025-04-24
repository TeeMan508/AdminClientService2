from src.user.exceptions.base import NoEntityException
from src.user.models import Admin
from src.user.schemas import AdminCredentials
from src.user.selectors import get_admin_


def admin__check_existing(client_creds: AdminCredentials):
    try:
        admin: Admin = get_admin_(tg_id=client_creds.tg_id)
        return True
    except NoEntityException:
        return False

