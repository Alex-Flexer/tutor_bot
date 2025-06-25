from datetime import datetime

from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext

from utils import keyboards as kb, captions
from routers.utils import TutorForm, CACHE_INTERVAL_EXPIRE, save_last_message, get_previous_message
from database import utils as db_utils

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
async def command_menu(message: Message, state: FSMContext) -> None:
    await save_last_message(message, state)

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
        datetime_allowed = await state.get_value("tutor_allowed")

        if datetime_allowed is None or datetime.now() - datetime_allowed > CACHE_INTERVAL_EXPIRE:

            last_msg = await message.edit_text(
                text=captions.INPUT_SK,
                reply_markup=kb.BACK_INLINE_KEYBOARD
            )
            await state.set_state(TutorForm.inputting_sk)
            await state.update_data(last_msg=last_msg)
        else:
            flag = True

            if role == "student":
                telegram_id = callback.from_user.id
                flag = db_utils.check_student_exists(telegram_id=telegram_id)

                if not flag:
                    await message.edit_text(
                        text=captions.NOT_STUDENT,
                        keyboard=kb.BACK_INLINE_KEYBOARD
                    )
            
            if flag:
                await message.edit_text(
                    text=captions.CHOOSE_STUDENT,
                    reply_markup=kb.get_students_inline_keyboard()
                )

    else:
        keyboard = getattr(kb, f"{role.upper()}_MENU_INLINE_KEYBOARD")

        await message.edit_text(
            text=captions.CHOOSE_OPTION,
            reply_markup=keyboard
        )

    await callback.answer()


@form_router.callback_query(F.data == "back")
async def process_back(callback: CallbackQuery, state: FSMContext):
    text, keyboard = await get_previous_message(state)
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


@form_router.message(default_state)
async def process_unknown_command(message: Message):
    await message.delete()
