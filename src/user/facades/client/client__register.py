from src.user.interactors import register_client_, register_admin_
from src.user.schemas import ClientCredentials, AdminCredentials


def client__register(creds: ClientCredentials):
    return register_client_(creds.tg_id, creds.complaint)