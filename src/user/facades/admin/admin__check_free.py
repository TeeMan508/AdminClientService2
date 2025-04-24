from src.user.exceptions.base import NoEntityException
from src.user.facades.admin import admin__get_random_free


def admin__check_free():
    try:
        admin__get_random_free()
        return True
    except NoEntityException:
        return False