from src.user.exceptions.base import NoEntityException
from src.user.models import  Client
from src.user.schemas import ClientCredentials
from src.user.selectors import get_client_


def client__check_existing(client_creds: ClientCredentials):
    try:
        client: Client = get_client_(tg_id=client_creds.tg_id)
        return True
    except NoEntityException:
        return False

