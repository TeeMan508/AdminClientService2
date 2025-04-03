from src.user.interactors import delete_client
from src.user.models import Admin
from src.user.schemas import AdminCredentials
from src.user.selectors import get_admin_sr_


def client__delete_by_admin(admin_creds: AdminCredentials):
    tarnished: Admin = get_admin_sr_(select_related="current_client", tg_id=admin_creds.tg_id).first()
    delete_client(tarnished.current_client)
