from src.user.models import Admin
from src.user.selectors import get_admin_, get_admin_sr_
from src.user.schemas import AdminCredentials
from src.user.interactors import free_admin, delete_client


def admin__free(admin_creds: AdminCredentials):
    tarnished = get_admin_(tg_id=admin_creds.tg_id)
    free_admin(tarnished)


