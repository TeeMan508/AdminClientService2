from uuid import uuid4

from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery
from aiogram import F
from aiohttp import ClientSession, ClientResponseError

from src.user.tasks.send_message import send_message
from .router import router
from ...logger import logger, correlation_id_ctx
from ...messages import ERROR_MESSAGE, REGISTER_ADMIN_MSG, NO_CLIENT_MSG
from ...schemas.send_to_service_request import SendToServiceRequest
from ...utils.correlated_client_session import ClientSessionCorId
from ...utils.send_to_service import send_to_service


class AdminState(StatesGroup):
    active = State()


@router.callback_query(F.data == "register_admin")
async def register_admin(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.message.from_user is None:
        return

    data = SendToServiceRequest.model_validate(
        {"tg_id": str(callback_query.message.chat.id),
         }
    )
    logger.info("Register admin request sent")
    await send_to_service(data)

    await state.set_state(AdminState.active)
    # await callback_query.message.edit_text(REGISTER_ADMIN_MSG)
    try:
        await callback_query.message.edit_reply_markup(None)
    except TelegramBadRequest:
        ...



