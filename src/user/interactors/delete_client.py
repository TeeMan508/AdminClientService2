from src.user.models import Client


def delete_client(client: Client):
    client.delete()