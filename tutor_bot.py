import asyncio
import logging
import sys
from secrets import token_urlsafe

from dotenv import dotenv_values, set_key

from aiogram import Bot, Dispatcher, Router, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand, Message
from aiogram.filters import Command

from utils import captions


form_router = Router()

BOT_COMMANDS = [
    BotCommand(command="gen_token", description="Generate secrete token")
]

ENV_PATH = ".env"

config = dotenv_values(ENV_PATH)

TOKEN = config["TUTOR_BOT_TOKEN"]
ALLOWED_TUTORS_ID = map(int, config["ALLOWED_TUTORS_ID"].split(";"))


@form_router.message(Command("gen_token"))
async def process_gen_token(message: Message):
    user_id = message.from_user.id
    if user_id not in ALLOWED_TUTORS_ID:
        return

    secret_key = token_urlsafe(25)
    set_key(ENV_PATH, "TUTOR_SECRET_KEY", secret_key)
    await message.answer(captions.GEN_KEY.format(html.code(secret_key)))


async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await bot.set_my_commands(commands=BOT_COMMANDS)

    dp = Dispatcher()
    dp.include_router(form_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout)
    asyncio.run(main())
