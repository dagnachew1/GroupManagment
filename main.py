import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from middleware.throttling import ThrottlingMiddleware#noqa
from handlers import get_handlers_router
from config import config

import coloredlogs

async def main():
    coloredlogs.install(level=config.logging.level)
    bot = Bot(
        token=config.telegram.api_token, 
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher(storage=MemoryStorage())
    
    dp["config"] = config
    
    #dp.message.middleware(ThrottlingMiddleware(rate_limit=config.telegram.rate_limit)) not needed for now
    dp.include_router(get_handlers_router())

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())