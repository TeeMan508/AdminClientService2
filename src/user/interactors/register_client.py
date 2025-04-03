from django.db import IntegrityError
from starlette.exceptions import HTTPException

from ..exceptions.base import AlreadyExistsException
from ..models import Client


def register_client_(client_id: str, complaint: str):
    try:
        Client.objects.create(tg_id=client_id, complaint=complaint)
    except IntegrityError:
        raise AlreadyExistsException("Client already exists")