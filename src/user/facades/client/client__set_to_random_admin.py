from src.user.interactors import set_client_to_admin
from src.user.selectors import get_client_
from .client__get_unhandled import get_random_free_admin


def client__set_to_random_admin(client_id: str):
    tarnished = get_random_free_admin()
    client = get_client_(tg_id=client_id)

    set_client_to_admin(client, tarnished)

    return tarnished.tg_id
