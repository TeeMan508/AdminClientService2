from typing import Any, Literal

from aiohttp import ClientResponseError

from .correlated_client_session import ClientSessionCorId
from ..logger import logger
from ..schemas.send_to_service_request import SendToServiceRequest
from ..urls import SERVICE_URL

async def send_to_service(data: SendToServiceRequest | None=None, type_: Literal['post', 'get']='post'):
    async with ClientSessionCorId() as session:
        if type_ == 'post':
            if not data:
                raise ValueError('Data cannot be empty on post request')

            async with session.post(SERVICE_URL, data=data.model_dump()) as response:
                response.raise_for_status()
                return await response.json()

        if type_ == 'get':
            if data:
                raise ValueError('Data should be empty on get request')

            async with session.get(SERVICE_URL) as response:
                response.raise_for_status()
                return await response.json()
            