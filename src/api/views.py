from starlette.exceptions import HTTPException
from pydantic import ValidationError
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .logger import logger, correlation_id_ctx
from ..user.exceptions.base import NoEntityException, BusyAdminException, AlreadyExistsException
from ..user.facades import admin__get_current_client, client__set_to_random_admin
from ..user.facades.admin import admin__register, admin__free, admin__get_by_client, admin__set_next_client
from ..user.facades.client import client__register, client__delete_by_admin
from ..user.schemas.request import (RegisterAdminRequestData,
                                    RegisterClientRequestData,
                                    SetClientToAdminRequestData,
                                    FreeAdminRequestData,
                                    GetClientRequestData,
                                    GetAdminByClientRequestData,
                                    SetNextClientRequestData,
                                    )
from ..user.schemas.domain import AdminCredentials, ClientCredentials
from ..user.schemas.response import EmptyResponseData, IdResponseData, ComplaintResponse


class RegisterAdminView(APIView):
    def post(self, request: Request): # noqa
        try:
            correlation_id_ctx.set(request.META.get('HTTP_X_CORRELATION_ID'))

            body = RegisterAdminRequestData.model_validate(request.POST.dict())
            creds = AdminCredentials.model_validate(body.model_dump())
            admin__register(creds)

            logger.info("Admin registered.")
            return Response(EmptyResponseData().model_dump(), status=status.HTTP_200_OK)

        except AlreadyExistsException:
            logger.info("Admin already registered.")
            return Response(EmptyResponseData().model_dump(), status=status.HTTP_409_CONFLICT)
        except ValidationError:
            logger.info("Wrong request format.")
            return Response(EmptyResponseData().model_dump(), status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class RegisterClientView(APIView):
    def post(self, request: Request): # noqa
        try:
            correlation_id_ctx.set(request.META.get('HTTP_X_CORRELATION_ID'))

            body = RegisterClientRequestData.model_validate(request.POST.dict())
            creds = ClientCredentials.model_validate(body.model_dump())
            client__register(creds)

            logger.info("Client registered.")
            return Response(EmptyResponseData().model_dump(), status=status.HTTP_200_OK)

        except AlreadyExistsException:
            logger.info("Client already registered.")
            return Response(EmptyResponseData().model_dump(), status=status.HTTP_409_CONFLICT)
        except ValidationError:
            logger.info("Wrong request format.")
            return Response(EmptyResponseData().model_dump(), status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class SetClientToRandomAdminView(APIView):
    def post(self, request: Request): # noqa
        try:
            correlation_id_ctx.set(request.META.get('HTTP_X_CORRELATION_ID'))

            body = SetClientToAdminRequestData.model_validate(request.POST.dict())
            admin_id = client__set_to_random_admin(body.tg_id)
            response_model = IdResponseData.model_validate({"tg_id": admin_id})

            logger.info("Client set to admin.")
            return Response(response_model.model_dump(), status=status.HTTP_200_OK)

        except NoEntityException:
            logger.info("No free admins.")
            return Response(EmptyResponseData().model_dump(), status=status.HTTP_409_CONFLICT)
        except ValidationError:
            logger.info("Wrong request format.")
            return Response(EmptyResponseData().model_dump(), status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class FreeAdminView(APIView):
    def post(self, request: Request): # noqa
        try:
            correlation_id_ctx.set(request.META.get('HTTP_X_CORRELATION_ID'))

            body = FreeAdminRequestData.model_validate(request.POST.dict())
            admin__free(AdminCredentials(tg_id=body.tg_id))

            logger.info("Admin free.")
            return Response(EmptyResponseData().model_dump(), status=status.HTTP_200_OK)
        except NoEntityException:
            logger.info("No such admin.")
            return Response(EmptyResponseData().model_dump(), status=status.HTTP_409_CONFLICT)
        except ValidationError:
            logger.info("Wrong request format.")
            return Response(EmptyResponseData().model_dump(), status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class ClearClientView(APIView):
    def post(self, request: Request):  # noqa
        try:
            correlation_id_ctx.set(request.META.get('HTTP_X_CORRELATION_ID'))

            body = FreeAdminRequestData.model_validate(request.POST.dict())
            client__delete_by_admin(AdminCredentials(tg_id=body.tg_id))

            logger.info("client deleted.")
            return Response(EmptyResponseData().model_dump(), status=status.HTTP_200_OK)
        except NoEntityException:
            logger.info("No such client.")
            return Response(EmptyResponseData().model_dump(), status=status.HTTP_409_CONFLICT)
        except ValidationError:
            logger.info("Wrong request format.")
            return Response(EmptyResponseData().model_dump(), status=status.HTTP_422_UNPROCESSABLE_ENTITY)

class GetCurrentClientView(APIView):
    def get(self, request: Request): # noqa
        try:
            correlation_id_ctx.set(request.META.get('HTTP_X_CORRELATION_ID'))

            body = GetClientRequestData.model_validate(request.data.dict())
            client_id = admin__get_current_client(body.tg_id)
            response_model = IdResponseData.model_validate({"tg_id": client_id})

            logger.info("Client found.")
            return Response(response_model.model_dump(), status=status.HTTP_200_OK)

        except NoEntityException:
            logger.info("No current client.")
            return Response(EmptyResponseData().model_dump(), status=status.HTTP_409_CONFLICT)
        except ValidationError:
            logger.info("Wrong request format.")
            return Response(EmptyResponseData().model_dump(), status=status.HTTP_422_UNPROCESSABLE_ENTITY)



class GetAdminByClientView(APIView):
    def get(self, request: Request): # noqa
        try:
            correlation_id_ctx.set(request.META.get('HTTP_X_CORRELATION_ID'))

            body = GetAdminByClientRequestData.model_validate(request.data.dict())
            admin_id = admin__get_by_client(body.tg_id)
            response_model = IdResponseData.model_validate({"tg_id": admin_id})

            logger.info("Admin found.")
            return Response(response_model.model_dump(), status=status.HTTP_200_OK)

        except NoEntityException:
            logger.info(f"No such admin found for client")
            return Response(EmptyResponseData().model_dump(), status=status.HTTP_409_CONFLICT)
        except ValidationError:
            logger.info("Wrong request format.")
            return Response(EmptyResponseData().model_dump(), status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class SetNextClientToAdminView(APIView):
    def post(self, request: Request): # noqa
        try:
            correlation_id_ctx.set(request.META.get('HTTP_X_CORRELATION_ID'))

            body = SetNextClientRequestData.model_validate(request.POST.dict())
            complaint = admin__set_next_client(body.tg_id)
            response_model = ComplaintResponse.model_validate({"complaint": complaint})
            logger.info("Next client set to admin.")
            return Response(response_model.model_dump(), status=status.HTTP_200_OK)

        except NoEntityException:
            logger.info("No unhandled clients.")
            return Response(EmptyResponseData().model_dump(), status=status.HTTP_409_CONFLICT)
        except BusyAdminException:
            logger.info("Admin is still busy.")
            return Response(EmptyResponseData().model_dump(), status=status.HTTP_409_CONFLICT)
        except ValidationError:
            logger.info("Wrong request format.")
            return Response(EmptyResponseData().model_dump(), status=status.HTTP_422_UNPROCESSABLE_ENTITY)