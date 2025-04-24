from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.handlers.callback.client import ClientState
from bot.handlers.command.router import router
from bot.messages import REGISTER_CLIENT_MSG
from bot.schemas.send_to_service_request import SendToServiceRequest
from bot.utils.send_to_service import send_to_service


@router.message(ClientState.active)
async def register_complaint(message: Message, state: FSMContext) -> None:
    if message.from_user is None:
        return


    data = SendToServiceRequest.model_validate(
        {"tg_id": str(message.chat.id),
         "complaint": message.text,
         }
    )
    await send_to_service(data)

    await message.answer(REGISTER_CLIENT_MSG)

