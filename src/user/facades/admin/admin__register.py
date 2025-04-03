from src.user.interactors import register_admin_
from src.user.schemas import AdminCredentials


def admin__register(creds: AdminCredentials):
    return register_admin_(creds.tg_id)