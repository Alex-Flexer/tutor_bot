import random
import os
import secrets
from datetime import datetime

import dotenv

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.types import (
    Message,
    FSInputFile,
    CallbackQuery,
    InputMediaPhoto
)
from aiogram.exceptions import TelegramBadRequest

from utils import keyboards as kb, captions
from database import utils as db_utils
from routers.utils import TutorForm, save_last_message, ENV_PATH, clear_media_group


async def check_student_id(
    callback_or_message: CallbackQuery | Message,
    state: FSMContext
) -> int | None:
    student_id = await state.get_value("student_id")
    callback_mode = isinstance(callback_or_message, CallbackQuery)
    message = callback_or_message.message if callback_mode else callback_or_message

    if student_id is None:
        await message.edit_text(
            text=captions.CHOOSE_STUDENT,
            reply_markup=kb.get_students_inline_keyboard()
        )
        if callback_mode:
            await callback_or_message.answer()

    return student_id

form_router = Router()


@form_router.message(TutorForm.inputting_sk)
async def process_input_sk(message: Message, state: FSMContext):
    user_sk = message.text
    sk = dotenv.get_key(ENV_PATH, "TUTOR_SECRET_KEY")

    last_msg = await state.get_value("last_msg")
    method = message.answer if last_msg is None else last_msg.edit_text

    if user_sk == sk:
        await method(
            text=captions.CHOOSE_STUDENT,
            reply_markup=kb.get_students_inline_keyboard()
        )
        await state.update_data(tutor_allowed=datetime.now())
        await state.set_state()

    elif last_msg.text != captions.INPUT_SK_AGAIN:
        last_msg = await method(
            text=captions.INPUT_SK_AGAIN,
            reply_markup=kb.BACK_INLINE_KEYBOARD
        )
        await state.update_data(last_msg=last_msg)

    await state.set_state()
    await message.delete()


@form_router.callback_query(F.data.startswith("tutor_select_"))
async def process_choose_student(callback: CallbackQuery, state: FSMContext):
    await save_last_message(callback.message, state)

    student_id = callback.data.removeprefix("tutor_select_")
    await state.update_data(student_id=student_id)

    await callback.message.edit_text(
        text=captions.CHOOSE_OPTION,
        reply_markup=kb.TUTOR_OPTION_INLINE_KEYBOARD
    )

    await callback.answer()


@form_router.callback_query(F.data == "tutor_hw")
async def process_tutor_hw(callback: CallbackQuery, state: FSMContext):
    student_id = await check_student_id(callback, state)
    if student_id is None:
        return

    await save_last_message(callback.message, state)

    await callback.message.edit_text(
        text=captions.CHOOSE_OPTION,
        reply_markup=kb.TUTOR_HW_INLINE_KEYBOARD
    )


@form_router.callback_query(F.data == "tutor_check_hw")
async def process_check_hw(callback: CallbackQuery, state: FSMContext):
    student_id = await check_student_id(callback, state)
    if student_id is None:
        return

    await save_last_message(callback.message, state)

    homeworks = db_utils.get_homeworks(student_id=student_id, submitted=True, checked=False)

    if homeworks:
        dates = db_utils.homeworks_to_str_dates(homeworks)
        await callback.message.edit_text(
            text=captions.CHOOSE_DATE,
            reply_markup=kb.get_homework_dates_inline_keyboard(
                dates=dates,
                mode="tutor"
            )
        )
    else:
        await callback.message.edit_text(
            text=captions.EMPTY,
            reply_markup=kb.BACK_INLINE_KEYBOARD
        )
    await callback.answer()


@form_router.callback_query(F.data == "tutor_set_hw")
async def process_set_hw(callback: CallbackQuery, state: FSMContext):
    student_id = await check_student_id(callback, state)
    if student_id is None:
        return

    await save_last_message(callback.message, state)

    await callback.message.edit_text(
        text=captions.CHOOSE_OPTION,
        reply_markup=kb.TUTOR_OPTION_INLINE_KEYBOARD
    )

    await callback.answer()


@form_router.callback_query(F.data == "tutor_update_probe")
async def process_update_probe(callback: CallbackQuery, state: FSMContext):
    student_id = await check_student_id(callback, state)
    if student_id is None:
        return

    await save_last_message(callback.message, state)

    homeworks = db_utils.get_homeworks(student_id=student_id)
    dates = db_utils.homeworks_to_str_dates(homeworks)

    await callback.message.edit_text(
        text=captions.CHOOSE_DATE,
        reply_markup=kb.get_homework_dates_inline_keyboard(
            dates=dates,
            mode="tutor"
        )
    )

    await callback.answer()


@form_router.callback_query(F.data.startswith("homework_tutor_"))
async def process_choose_task_date(callback: CallbackQuery, state: FSMContext):
    student_id = await check_student_id(callback, state)
    if student_id is None:
        return

    await save_last_message(callback.message, state)

    mode = "submitted"
    date = callback.data.removeprefix("homework_tutor_")

    images_path = db_utils.IMAGES_PATH.format(student_id, date, mode)
    photos = os.listdir(images_path)

    with open(
        file=db_utils.COMMENT_PATH.format(student_id, date, mode),
        mode='r',
        encoding='utf-8'
    ) as comment_file:
        comment = comment_file.read()

    if not comment:
        comment = captions.EMPTY_STUDENT_COMMENT

    caption = captions.STUDENT_COMMENT.format(comment)

    if photos:
        media_builder = MediaGroupBuilder(caption=caption)

        for photo in photos:
            media_builder.add(
                type="photo",
                media=FSInputFile(os.path.join(images_path, photo))
            )
        media_group = await callback.message.answer_media_group(media=media_builder.build())
    else:
        media_group = await callback.message.answer(caption)

    await state.update_data(media_group=media_group)

    feedback_text_message = await callback.message.answer(
        text=captions.SUBMIT_FEEDBACK,
        reply_markup=kb.BACK_INLINE_KEYBOARD
    )

    await state.update_data(feedback_text_message=feedback_text_message)

    await state.update_data(hw_date=date)
    await state.set_state(TutorForm.checking_hw)

    await callback.message.delete()
    await callback.answer()


@form_router.message(TutorForm.checking_hw)
async def process_upload_feedback(message: Message, state: FSMContext):
    student_id = await check_student_id(message, state)
    if student_id is None:
        return

    hw_date = await state.get_value("hw_date")
    mode = "feedback"

    if message.photo is not None:
        image_path = os.path.join(
            db_utils.IMAGES_PATH.format(student_id, hw_date, mode),
            f"{secrets.token_urlsafe(5)}.png"
        )

        await message.bot.download(
            file=message.photo[-1].file_id,
            destination=image_path
        )

    comment = (
        message.caption
        if message.caption is not None
        else (
            ""
            if message.text is None
            else message.text
        )
    )

    with open(
        file=db_utils.COMMENT_PATH.format(student_id, hw_date, mode),
        mode='w',
        encoding="utf-8"
    ) as comment_file:
        comment_file.write(comment)

    hw_submitted = db_utils.set_checked_homework(
        student_id=student_id,
        homework_date=datetime.strptime(hw_date, "%d.%m.%Y")
    )

    feedback_text_message = await state.get_value("feedback_text_message")

    method = (
        message.answer
        if feedback_text_message is None
        else feedback_text_message.edit_text
    )

    caption = (
        captions.DATA_UPDATED_SUCCESS
        if hw_submitted
        else captions.DATA_UPDATED_FAILED
    )

    try:
        feedback_text_message = await method(
            text=caption,
            reply_markup=kb.BACK_INLINE_KEYBOARD
        )
    except TelegramBadRequest:
        pass
    finally:
        await state.update_data(feedback_text_message=feedback_text_message)

        await state.set_state()
        await message.delete()
        await clear_media_group(state)
