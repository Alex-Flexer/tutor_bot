from datetime import datetime

import dotenv

from aiogram import Router, F, html
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext

from database import utils as db_utils
from utils import (
    keyboards as kb, captions,
    save_last_message, get_previous_message,
    ENV_PATH
)


form_router = Router()


@form_router.message(CommandStart())
async def command_start(message: Message) -> None:
    photo = FSInputFile("./images/start_img.jpg")
    await message.answer_photo(
        photo,
        captions.HELLO_TEXT
    )


@form_router.message(Command("myid"))
async def command_start(message: Message) -> None:
    await message.answer(captions.MY_ID.format(html.code(message.from_user.id)))


@form_router.message(Command("contacts"))
async def command_contacts(message: Message) -> None:
    await message.answer(captions.CONTACTS_TEXT)


@form_router.message(Command("menu"))
async def command_menu(message: Message, state: FSMContext) -> None:
    await message.answer(
        text=captions.CHOOSE_ROLE,
        reply_markup=kb.MAIN_MENU_INLINE_KEYBOARD
    )


@form_router.callback_query(F.data.startswith("i_am_"))
async def process_i_am(callback: CallbackQuery, state: FSMContext) -> None:
    await save_last_message(callback.message, state)

    role = callback.data.lstrip("i_am_")
    message = callback.message

    if role == "tutor":
        allowed_tutors_id = map(int, dotenv.get_key(ENV_PATH, "ALLOWED_TUTORS_ID").split(";"))
        user_id = callback.from_user.id
        
        if user_id not in allowed_tutors_id:
            await callback.message.edit_text(
                text=captions.NOT_TUTOR,
                reply_markup=kb.BACK_INLINE_KEYBOARD
            )
        else:
            await message.edit_text(
                text=captions.CHOOSE_OPTION,
                reply_markup=kb.TUTOR_MENU_INLINE_KEYBOARD
            )

    elif role == "student":
        telegram_id = callback.from_user.id

        if not db_utils.check_student_exists(telegram_id=telegram_id):
            await message.edit_text(
                text=captions.NOT_STUDENT,
                reply_markup=kb.BACK_INLINE_KEYBOARD
            )
        else:
            await message.edit_text(
                text=captions.CHOOSE_STUDENT,
                reply_markup=kb.STUDENT_MENU_INLINE_KEYBOARD
            )

    else:
        await message.edit_text(
            text=captions.CHOOSE_OPTION,
            reply_markup=kb.PARENT_MENU_INLINE_KEYBOARD
        )

    await callback.answer()


@form_router.callback_query(F.data == "back")
async def process_back(callback: CallbackQuery, state: FSMContext):
    text, keyboard = await get_previous_message(state)
    await callback.message.edit_text(text, reply_markup=keyboard)
    await state.set_state()
    await callback.answer()


@form_router.message(default_state)
async def process_unknown_command(message: Message):
    await message.delete()
