from queue import deque

import dotenv
import secrets
import asyncio

from aiogram import Router, F, html
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext

from database import utils as db_utils
from utils import (
    keyboards as kb, captions,
    get_previous_message,
    send_mailing,
    ENV_PATH
)


form_router = Router()


@form_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    parts = message.text.split()
    if len(parts) == 2:
        user_sk = parts[1]
        real_sk = dotenv.get_key(ENV_PATH, "TUTOR_SECRET_KEY")

        if user_sk == real_sk:
            str_allowed_tutors_id = dotenv.get_key(ENV_PATH, "ALLOWED_TUTORS_ID")
            allowed_tutors_id = list(str_allowed_tutors_id.split(";")) if str_allowed_tutors_id else []

            user_id = str(message.from_user.id)

            if user_id not in allowed_tutors_id:
                allowed_tutors_id.append(user_id)
                joined_allowed_tutors_id = ";".join(allowed_tutors_id)
                dotenv.set_key(ENV_PATH, "ALLOWED_TUTORS_ID", joined_allowed_tutors_id)

            dotenv.set_key(ENV_PATH, "TUTOR_SECRET_KEY", secrets.token_urlsafe(15))

    photo = FSInputFile("./images/start_img.jpg")
    await message.answer_photo(
        photo,
        captions.HELLO_TEXT,
        reply_markup=kb.MAIN_MENU_INLINE_KEYBOARD
    )
    await state.update_data(msg_history=deque())

@form_router.message(Command("contacts"))
async def command_contacts(message: Message) -> None:
    await message.answer(captions.CONTACTS_TEXT)


@form_router.message(Command("menu"))
async def command_menu(message: Message, state: FSMContext) -> None:
    await message.answer(
        text=captions.CHOOSE_ROLE,
        reply_markup=kb.MAIN_MENU_INLINE_KEYBOARD
    )
    await state.update_data(msg_history=deque())


@form_router.message(Command("i_am_tutor"))
async def command_menu(message: Message, state: FSMContext) -> None:
    allowed_tutors_id = map(int, dotenv.get_key(ENV_PATH, "ALLOWED_TUTORS_ID").split(";"))
    user_id = message.from_user.id
    
    if user_id not in allowed_tutors_id:
        await message.answer(
            text=captions.NOT_TUTOR,
            reply_markup=None
        )
    else:
        await message.answer(
            text=captions.CHOOSE_OPTION,
            reply_markup=kb.TUTOR_MENU_INLINE_KEYBOARD
        )
        await state.update_data(msg_history=deque())


@form_router.callback_query(F.data.startswith("i_am_"))
async def process_i_am(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(msg_history=deque([(captions.CHOOSE_ROLE, kb.MAIN_MENU_INLINE_KEYBOARD)]))

    role = callback.data.lstrip("i_am_")
    message = callback.message
    
    method = message.edit_text
    
    if message.photo is not None:
        await callback.message.delete()
        method = message.answer

    if role == "student":
        telegram_id = callback.from_user.id

        if not db_utils.check_student_exists(telegram_id=telegram_id):
            asyncio.create_task(send_mailing(callback))
            
            text = captions.NOT_STUDENT.format(html.code(telegram_id))
            reply_markup = kb.BACK_INLINE_KEYBOARD

        else:
            text = captions.CHOOSE_STUDENT
            reply_markup = kb.STUDENT_MENU_INLINE_KEYBOARD

    else:
        text = captions.CHOOSE_OPTION
        reply_markup = kb.PARENT_MENU_INLINE_KEYBOARD
        
    await method(text=text, reply_markup=reply_markup)

    await callback.answer()


@form_router.callback_query(F.data.startswith("back_"))
async def process_back(callback: CallbackQuery, state: FSMContext):
    k = int(callback.data.removeprefix("back_"))

    text, keyboard = await get_previous_message(state, k)
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


@form_router.message(default_state)
async def process_unknown_command(message: Message):
    await message.delete()
