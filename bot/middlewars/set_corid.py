from typing import Callable, Any, Awaitable, Dict
from uuid import uuid4

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from bot.logger import correlation_id_ctx


class SetCorIdMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
        ):
        correlation_id_ctx.set(str(uuid4()))

        result = await handler(event, data)
        return result