from src.user.selectors import get_client_, get_admin_

def client__get_unhandled():
    return get_client_(order_by="created_at", is_handling=False)

