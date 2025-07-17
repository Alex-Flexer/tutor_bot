import re

from aiogram import Router, F, html
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    CallbackQuery
)

from database import utils as db_utils
from utils import (
    keyboards as kb, captions,
    ParentForm,
    save_last_message,
    get_last_homeworks_str
)

form_router = Router()

# ======================================================================
# ------------------------------LESSON BLOCK----------------------------
# ======================================================================


@form_router.callback_query(F.data == "parent_sign_up_lesson")
async def process_student_info(callback: CallbackQuery, state: FSMContext):
    await save_last_message(callback.message, state)

    last_msg = await callback.message.edit_text(
        text=captions.INPUT_EMAIL,
        reply_markup=kb.ADD_LESSON_INLINE_KEYBOARD
    )

    await state.update_data(last_msg=last_msg)
    await state.set_state(ParentForm.inputting_email)

    await callback.answer()


@form_router.message(ParentForm.inputting_email)
async def process_input_sk(message: Message, state: FSMContext):

    def is_valid_email(email: str) -> bool:
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return re.match(pattern, email) is not None and len(email) < 80

    last_msg = await state.get_value("last_msg")
    method = message.answer if last_msg is None else last_msg.edit_text

    email = message.text
    username = '@' + message.from_user.username

    if not is_valid_email(email):
        if last_msg is None or last_msg.text != captions.INCORRECT_EMAIL:
            last_msg = await method(
                text=captions.INCORRECT_EMAIL,
                reply_markup=kb.BACK_INLINE_KEYBOARD
            )
            await state.update_data(last_msg=last_msg)
    else:
        lesson_added = db_utils.add_lesson(username, email=email)

        await method(
            text=(
                captions.LESSON_ADD_SUCCESS
                if lesson_added
                else captions.LESSON_ADD_FAILED
            ),
            reply_markup=kb.BACK_INLINE_KEYBOARD
        )

        await state.set_state()

    await message.delete()


@form_router.callback_query(F.data == "another_way_sign_up_lesson")
async def process_student_info(callback: CallbackQuery, state: FSMContext):
    await save_last_message(callback.message, state)

    last_msg = await callback.message.edit_text(
        text=captions.INPUT_CONTACT_DATA,
        reply_markup=kb.DOUBLE_BACK_INLINE_KEYBOARD
    )

    await state.update_data(last_msg=last_msg)
    await state.set_state(ParentForm.inputting_other_data)

    await callback.answer()


@form_router.message(ParentForm.inputting_other_data)
async def process_input_sk(message: Message, state: FSMContext):
    last_msg = await state.get_value("last_msg")
    method = message.answer if last_msg is None else last_msg.edit_text

    other_data = message.text
    username = '@' + message.from_user.username

    if len(other_data) >= 80:
        if last_msg is None or last_msg.text != captions.INCORRECT_CONTACT_DATA:
            last_msg = await method(
                text=captions.INCORRECT_CONTACT_DATA,
                reply_markup=kb.DOUBLE_BACK_INLINE_KEYBOARD
            )
            await state.update_data(last_msg=last_msg)
    else:
        lesson_added = db_utils.add_lesson(username, other_data=other_data)

        await method(
            text=(
                captions.LESSON_ADD_SUCCESS
                if lesson_added
                else captions.LESSON_ADD_FAILED
            ),
            reply_markup=kb.DOUBLE_BACK_INLINE_KEYBOARD
        )
        await state.set_state()

    await message.delete()


# ======================================================================
# -----------------------------STUDENT BLOCK----------------------------
# ======================================================================

@form_router.callback_query(F.data == "parent_student_info")
async def process_student_info(callback: CallbackQuery, state: FSMContext):
    await save_last_message(callback.message, state)

    last_msg = await callback.message.edit_text(
        text=captions.PARENT_INPUT_STUDENT_ID,
        reply_markup=kb.BACK_INLINE_KEYBOARD
    )

    await state.update_data(last_msg=last_msg)
    await state.set_state(ParentForm.inputting_student_id)

    await callback.answer()


@form_router.message(ParentForm.inputting_student_id)
async def process_input_sk(message: Message, state: FSMContext):
    last_msg = await state.get_value("last_msg")
    method = message.answer if last_msg is None else last_msg.edit_text

    student_id = message.text
    student = db_utils.get_student(student_id=student_id)

    if student is None:
        if last_msg is None or last_msg.text != captions.INCORRECT_STUDENT_ID:
            last_msg = await method(
                text=captions.INCORRECT_STUDENT_ID,
                reply_markup=kb.BACK_INLINE_KEYBOARD
            )
            await state.update_data(last_msg=last_msg)
    else:
        homeworks_str = get_last_homeworks_str(student_id=student_id)

        await method(
            text=captions.PARENT_STUDENT_PROFILE_TEXT.format(
                student.name,
                student.surname,
                html.code(student.student_id),
                "undefined" if student.last_probe_result is None else student.last_probe_result,
                homeworks_str,
                html.link(captions.GD_LINK, student.gd_link)
            ),
            reply_markup=kb.BACK_INLINE_KEYBOARD
        )

    await message.delete()
