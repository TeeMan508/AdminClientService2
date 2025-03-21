from ..selectors import get_admin_, get_admin_sr_
from ..schemas import AdminCredentials



def free_admin(admin_creds: AdminCredentials):
    tarnished = get_admin_(tg_id=admin_creds.tg_id).first()

    tarnished.is_busy = False
    tarnished.save()

def clear_client_by_admin_creds(admin_creds: AdminCredentials):
    tarnished = get_admin_sr_(select_related="current_client", tg_id=admin_creds.tg_id).first()

    tarnished.current_client.delete()


