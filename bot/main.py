import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from conf.config import settings
from handlers.auth.auth import AuthMiddleware, register_handlers_auth


async def main():
    api_token = settings.BOT_TOKEN

    logging.basicConfig(level=logging.DEBUG)
    storage = RedisStorage2('redis', 6379, db=5, pool_size=10, prefix='state')

    bot = Bot(token=api_token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    dp.middleware.setup(AuthMiddleware())

    register_handlers_auth(dp)

    # await set_commands(bot)
    await dp.skip_updates()
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
