from uuid import uuid4

from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiohttp import ClientSession, ClientResponseError

from .router import router

from ...bot import bot
from ...logger import logger, correlation_id_ctx
from ...messages import ERROR_MESSAGE, REGISTER_CLIENT_MSG, NO_ADMIN_MSG
from ...urls import REGISTER_CLIENT_URL, SET_CLIENT_TO_ADMIN_URL
from ..callback.client import ClientState
from ...utils.correlated_client_session import ClientSessionCorId


@router.message(ClientState.active)
async def register_client_and_send_complaint(message: Message, state: FSMContext) -> None:
    if message.from_user is None:
        return

    await message.answer(REGISTER_CLIENT_MSG)

    body = {
        "complaint" : message.text,
        "tg_id": str(message.chat.id),
    }

    # TODO: надо разделить удаление клиента и освобождение админа - удалять в handle_complaint а освобождать в next_client
    logger.info("Registering client...")
    async with ClientSessionCorId() as session:
        async with session.post(url=REGISTER_CLIENT_URL, data=body) as response:
            try:
                response.raise_for_status()
            except ClientResponseError as e:
                text = f"{ERROR_MESSAGE}: {e}"
                await message.answer(text)
                return

    logger.info("Setting client to admin...")
    async with ClientSessionCorId() as session:
        async with session.post(url=SET_CLIENT_TO_ADMIN_URL, data=body) as response:
            try:
                response.raise_for_status()
                data = await response.json()
                await bot.send_message(int(data["tg_id"]), body["complaint"])
            except ClientResponseError as e:
                text = f"{NO_ADMIN_MSG}"
                await message.answer(text)

    logger.info("Client registered.")
    await state.set_state(ClientState.registered)