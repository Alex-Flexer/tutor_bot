from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, FSInputFile

    
form_router = Router()

    
HELLO_TEXT = """👋 Привет!
Ты в умном боте для подготовки к ЕГЭ и ОГЭ математике.

Здесь ты сможешь:
✅ Проверить свои ответы.
✅ Получишь консультацию через кнопку «контакты»

🚀 Просто выберете номер варианта и отправь свой ответ — бот всё проверит!
И помни: каждая ошибка — это шаг к 100 баллам.

Готов проверить себя? Погнали! 🎯
"""


CONTACTS_TEXT = """Поддержка:

Присоединяйтесь к нашему Telegram-каналу:
@matnas7

💬 Если у вас есть вопросы или вам нужна помощь:
@NikitaAlekseevichh
"""



@form_router.message(CommandStart())
async def command_start(message: Message) -> None:
    photo = FSInputFile("./images/start_img.jpg")
    await message.answer_photo(
        photo,
        HELLO_TEXT
    )


@form_router.message(Command("contacts"))
async def command_contacts(message: Message) -> None:
    await message.answer(CONTACTS_TEXT)


@form_router.message()
async def process_unknown_command(message: Message):
    await message.answer("Неизвестная команда.")