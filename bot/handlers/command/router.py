from aiogram import Router

from bot.middlewars.set_corid import SetCorIdMiddleware

router = Router()
router.message.outer_middleware(SetCorIdMiddleware())