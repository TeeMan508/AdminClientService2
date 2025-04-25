from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.handlers.callback.admin import AdminState
from bot.handlers.command.router import router
from bot.logger import logger
from bot.messages import REGISTER_CLIENT_MSG
from bot.schemas.send_to_service_request import SendToServiceRequest
from bot.utils.send_to_service import send_to_service


@router.message(AdminState.active)
async def send_answer(message: Message, state: FSMContext) -> None:
    if message.from_user is None:
        return

    data = SendToServiceRequest.model_validate(
        {"tg_id": str(message.chat.id),
         "response": message.text,
         }
    )
    logger.info("Sending answer from admin to service")

    await send_to_service(data)
