from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, FSInputFile, CallbackQuery

from utils import keyboards, captions

form_router = Router()



@form_router.message(CommandStart())
async def command_start(message: Message) -> None:
    photo = FSInputFile("./images/start_img.jpg")
    await message.answer_photo(
        photo,
        captions.HELLO_TEXT
    )


@form_router.message(Command("contacts"))
async def command_contacts(message: Message) -> None:
    await message.answer(captions.CONTACTS_TEXT)


@form_router.message(Command("menu"))
async def command_start(message: Message) -> None:
    photo = FSInputFile("./images/start_img.jpg")
    await message.answer(
        text=captions.CHOOSE_ROLE,
        reply_markup=keyboards.MAIN_MENU_INLINE_KEYBOARD
    )


@form_router.callback_query(F.data.startswith("i_am_"))
async def command_start(callback: CallbackQuery) -> None:
    role = callback.data.lstrip("i_am_")
    message = callback.message
    
    keyboard = getattr(keyboards, f"{role.upper()}_MENU_INLINE_KEYBOARD")
    
    await message.edit_text(captions.CHOOSE_OPTION)
    await message.edit_reply_markup(reply_markup=keyboard)
    
    await callback.answer()


@form_router.message()
async def process_unknown_command(message: Message):
    await message.answer()
