from aiogram import Router

from bot.middlewars.set_corid import SetCorIdMiddleware

router = Router()
router.callback_query.outer_middleware(SetCorIdMiddleware())
