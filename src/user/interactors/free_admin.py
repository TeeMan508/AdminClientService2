from src.user.models import Admin


def free_admin(admin: Admin):
    admin.is_busy = False
    admin.save()