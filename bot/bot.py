import asyncio
import logging
import locale

from aiogram import Bot, Dispatcher

from config import config
from handlers import common_handler, registration_handler


locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')


async def main():
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()

    dp.include_routers(common_handler.router, registration_handler.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
