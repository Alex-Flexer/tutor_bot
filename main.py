import asyncio
import logging
import sys

from dotenv import dotenv_values

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from routers import common_router, student_router


BOT_COMMANDS = [
    BotCommand(command="start", description="Start bot"),
    BotCommand(command="menu", description="Main menu"),
    BotCommand(command="contacts", description="Get contacts")
]


config = dotenv_values(".env")
TOKEN = config["TOKEN"]


async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await bot.set_my_commands(commands=BOT_COMMANDS)

    dp = Dispatcher()
    dp.include_router(student_router)
    dp.include_router(common_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout)
    asyncio.run(main())
