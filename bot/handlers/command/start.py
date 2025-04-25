from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiohttp import ClientSession

from .router import router
from ...logger import logger
from ...messages import REGISTER_TEXT
from ...urls import SERVICE_URL


@router.message(Command("start"))
async def handle_start_command(message: Message, state: FSMContext) -> None:
    if message.from_user is None:
        return
    logger.info("Session starts")

    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Client", callback_data="register_client"))
    builder.add(InlineKeyboardButton(text="Admin", callback_data="register_admin"))

    await message.answer(REGISTER_TEXT, reply_markup=builder.as_markup())



