from django.db.models import QuerySet
from starlette.exceptions import HTTPException

from ..exceptions.base import NoEntityException
from ..models import Admin


def get_admin_sr_(select_related="", **filters) -> QuerySet:
    admin_qs = Admin.objects.filter(**filters).select_related(select_related)

    admin: Admin = admin_qs.first()
    if not admin:
        raise NoEntityException("No admin found")

    return admin_qs
