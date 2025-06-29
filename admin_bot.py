import asyncio
# import logging
import sys
from secrets import token_urlsafe

from dotenv import dotenv_values, set_key, get_key

from aiogram import Bot, Dispatcher, Router, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand, Message
from aiogram.filters import Command

from utils import captions, ENV_PATH


form_router = Router()

BOT_COMMANDS = [
    BotCommand(command="get_url", description="Get current temp url")
]

config = dotenv_values(ENV_PATH)

TOKEN = config["ADMIN_BOT_TOKEN"]
ADMIN_ID = int(config["ADMIN_ID"])


@form_router.message(Command("get_url"))
async def process_gen_token(message: Message):
    user_id = message.from_user.id
    if user_id != ADMIN_ID:
        return

    secret_key = get_key(ENV_PATH, "TUTOR_SECRET_KEY")
    url = f"https://t.me/ege_botbotbot?start={secret_key}"
    await message.answer(captions.GEN_KEY.format(url))


async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await bot.set_my_commands(commands=BOT_COMMANDS)

    dp = Dispatcher()
    dp.include_router(form_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
