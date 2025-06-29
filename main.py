import asyncio
import logging
import sys
import os

from dotenv import dotenv_values

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from routers import common_router, student_router, tutor_router, parent_router


BOT_COMMANDS = [
    BotCommand(command="start", description="Start bot"),
    BotCommand(command="menu", description="Main menu"),
    BotCommand(command="contacts", description="Get contacts"),
    BotCommand(command="i_am_tutor", description="Tutor mode")
]


config = dotenv_values(".env")
TOKEN = config["MAIN_BOT_TOKEN"]


def set_script_dir():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    sys.path.insert(0, script_dir)


async def main():
    set_script_dir()

    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await bot.set_my_commands(commands=BOT_COMMANDS)

    dp = Dispatcher()
    dp.include_router(tutor_router)
    dp.include_router(student_router)
    dp.include_router(common_router)
    dp.include_router(parent_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout)
    asyncio.run(main())
