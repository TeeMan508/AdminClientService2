from pydantic import ValidationError
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .logger import logger

from ..user.exceptions.base import NoEntityException, BusyAdminException
from ..user.facades import client__set_to_random_admin, admin__get_current_client
from ..user.facades.admin import admin__check_free, admin__check_existing, admin__register, admin__set_next_client, \
    admin__free
from ..user.facades.client import client__register, client__check_existing, client__delete_by_admin
from ..user.schemas import ClientCredentials, AdminCredentials
from ..user.schemas.request import MainViewRequest
from ..user.schemas.response import EmptyResponseData
from ..user.tasks.send_message import send_message


class MainView(APIView):
    def post(self, request: Request): # noqa
        try:

            data = MainViewRequest.model_validate(request.POST.dict())
            # client handling
            if data.complaint:
                client_creds = ClientCredentials.model_validate(data.model_dump())
                if client__check_existing(client_creds):
                    return Response(EmptyResponseData().model_dump(), status=status.HTTP_200_OK)

                client__register(client_creds)

                if not admin__check_free():
                    logger.info("No free admins")
                    return Response(EmptyResponseData().model_dump(), status=status.HTTP_200_OK)

                admin_id = client__set_to_random_admin(client_creds.tg_id)
                send_message.delay(admin_id, client_creds.complaint)
                return Response(EmptyResponseData().model_dump(), status=status.HTTP_200_OK)

            # admin handling
            admin_creds = AdminCredentials.model_validate(data.model_dump())
            if not admin__check_existing(admin_creds):
                admin__register(admin_creds)
                try:
                    complaint = admin__set_next_client(admin_creds.tg_id)
                    send_message.delay(admin_creds.tg_id, complaint)
                except NoEntityException:
                    logger.info("No unhandled clients")
                    return Response(EmptyResponseData().model_dump(), status=status.HTTP_200_OK)

            if not admin_creds.response:
                return Response(EmptyResponseData().model_dump(), status=status.HTTP_200_OK)

            send_message.delay(admin__get_current_client(admin_creds.tg_id), admin_creds.response)
            admin__free(admin_creds)
            client__delete_by_admin(admin_creds)

            return Response(EmptyResponseData().model_dump(), status=status.HTTP_200_OK)




        except ValidationError:
            return Response(EmptyResponseData().model_dump(), status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except (NoEntityException, BusyAdminException):
            return Response(EmptyResponseData().model_dump(), status=status.HTTP_409_CONFLICT)
