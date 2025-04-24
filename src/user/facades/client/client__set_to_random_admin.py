from src.user.facades.admin import admin__get_random_free
from src.user.interactors import set_client_to_admin
from src.user.selectors import get_client_


def client__set_to_random_admin(client_id: str):
    tarnished = admin__get_random_free()
    client = get_client_(tg_id=client_id)

    set_client_to_admin(client, tarnished)

    return tarnished.tg_id
