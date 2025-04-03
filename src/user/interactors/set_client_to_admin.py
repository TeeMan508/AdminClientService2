from src.user.models import Admin, Client


def set_client_to_admin(client: Client, admin: Admin):
    admin.is_busy = True
    admin.current_client = client
    admin.save()

    client.is_handling = True
    client.save()