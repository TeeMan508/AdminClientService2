from src.user.selectors import get_admin_


def admin__get_random_free():
    return get_admin_(order_by='?', is_busy=False)
