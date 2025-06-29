from datetime import datetime
import secrets
import asyncio
import os

import dotenv

from aiogram import Router, F, html
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import (
    Message,
    FSInputFile,
    CallbackQuery
)

from database import utils as db_utils, Lesson
from utils import (
    keyboards as kb, captions,
    TutorForm,
    save_last_message, clear_media_group,
    lessons_to_text, check_student_id,
    ENV_PATH
)


form_router = Router()


# ======================================================================
# -----------------------------LESSONS BLOCK----------------------------
# ======================================================================


@form_router.callback_query(F.data == "tutor_lessons")
async def process_tutor_lessons(callback: CallbackQuery, state: FSMContext):
    await save_last_message(callback.message, state)
    lessons: list[Lesson] = sorted(db_utils.get_lessons(), key=lambda lesson: lesson.date)

    if not lessons:
        text = captions.EMPTY_LESSONS_LIST
    else:
        lessons_text = lessons_to_text(lessons)
        text = captions.LESSONS_LIST.format(lessons_text)

        await state.set_state(TutorForm.deleting_lesson)

    lessons_list_msg = await callback.message.edit_text(
        text=text,
        reply_markup=kb.BACK_INLINE_KEYBOARD
    )

    if lessons:
        await state.update_data(lessons_list_msg=lessons_list_msg)

    await callback.answer()


@form_router.message(F.text.regexp(r"^/del_\d+$"), TutorForm.deleting_lesson)
async def process_del_lesson(message: Message, state: FSMContext):
    lesson_id = message.text.split("_")[1]
    lessons_list_msg = await state.get_value("lessons_list_msg")

    await message.delete()

    method = (
        message.answer
        if lessons_list_msg is None
        else lessons_list_msg.edit_text
    )

    db_utils.delete_lesson(lesson_id)

    new_lessons = db_utils.get_lessons()

    if not new_lessons:
        new_text = captions.EMPTY_LESSONS_LIST
        await state.set_state()
    else:
        new_lessons_text = lessons_to_text(new_lessons)
        new_text = captions.LESSONS_LIST.format(new_lessons_text)

    await method(
        text=new_text,
        reply_markup=kb.BACK_INLINE_KEYBOARD
    )



# ======================================================================
# -----------------------------HOMEWORK BLOCK---------------------------
# ======================================================================


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
                mode="tutor_check"
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
        text=captions.CHOOSE_DATE,
        reply_markup=kb.get_dates_in_month_inline_keyboard()
    )

    await callback.answer()


@form_router.callback_query(F.data.startswith("homework_tutor_check_"))
async def process_choose_check_task_date(callback: CallbackQuery, state: FSMContext):
    student_id = await check_student_id(callback, state)
    if student_id is None:
        return

    await save_last_message(callback.message, state)

    mode = "submitted"
    date = callback.data.removeprefix("homework_tutor_check_")

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


@form_router.callback_query(F.data.startswith("tutor_set_hw_"))
async def process_choose_set_task_date(callback: CallbackQuery, state: FSMContext):
    student_id = await check_student_id(callback, state)
    if student_id is None:
        return

    await save_last_message(callback.message, state)

    date_str = callback.data.removeprefix("tutor_set_hw_")
    date = datetime.strptime(date_str, "%d.%m.%Y")

    print(date)

    if db_utils.check_hw_exists(student_id, date):
        print("hahaha")
        await callback.message.edit_text(
            text=captions.HOMEWORK_ALREADY_SET,
            reply_markup=kb.BACK_INLINE_KEYBOARD
        )

    else:
        print("bebebe")
        homework_text_message = await callback.message.edit_text(
            text=captions.TUTOR_SET_HOMEWORK,
            reply_markup=kb.BACK_INLINE_KEYBOARD
        )

        await state.update_data(hw_date=date_str)
        await state.update_data(homework_text_message=homework_text_message)
        await state.set_state(TutorForm.uploading_hw)

    await callback.answer()


@form_router.message(TutorForm.uploading_hw)
async def process_upload_homework(message: Message, state: FSMContext):
    student_id = await check_student_id(message, state)
    if student_id is None:
        return

    async def reset_data():
        await message.delete()
        await clear_media_group(state)

        await asyncio.sleep(2)

        await state.update_data(
            homework_text_message=None,
            hw_submitted=None,
            last_mgid=None
        )
        await state.set_state()

    hw_date = await state.get_value("hw_date")
    last_mgid = await state.get_value("last_mgid")
    hw_submitted = await state.get_value("hw_submitted")
    homework_text_message = await state.get_value("homework_text_message")

    mode = "homework"

    cur_mgid = message.media_group_id

    if last_mgid is not None and cur_mgid != last_mgid:
        await reset_data()
        return

    if hw_submitted is None:
        hw_submitted = db_utils.set_homework(
            student_id=student_id,
            homework_date=datetime.strptime(hw_date, "%d.%m.%Y")
        )
        await state.update_data(hw_submitted=hw_submitted)

    method = (
        message.answer
        if homework_text_message is None
        else homework_text_message.edit_text
    )

    caption = (
        captions.HW_SUBMITTED_SUCCESS
        if hw_submitted
        else captions.HW_SUBMITTED_FAILED
    )

    if not hw_submitted:
        await method(
            text=caption,
            reply_markup=kb.BACK_INLINE_KEYBOARD
        )
        await reset_data()
        return

    if message.photo is not None:
        image_path = os.path.join(
            db_utils.IMAGES_PATH.format(student_id, hw_date, mode),
            secrets.token_urlsafe(5) + ".png"
        )

        await message.bot.download(
            file=message.photo[-1].file_id,
            destination=image_path
        )

    comment = ""

    if message.caption is not None:
        comment = message.caption
    elif message.text is not None:
        comment = message.text

    with open(
        file=db_utils.COMMENT_PATH.format(student_id, hw_date, mode),
        mode='a',
        encoding="utf-8"
    ) as comment_file:
        comment_file.write(comment)

    try:
        homework_text_message = await method(
            text=caption,
            reply_markup=kb.BACK_INLINE_KEYBOARD
        )
    except TelegramBadRequest:
        pass
    finally:
        await state.update_data(
            homework_text_message=homework_text_message,
            last_mgid=cur_mgid
        )

        await reset_data()


@form_router.message(TutorForm.checking_hw)
async def process_upload_feedback(message: Message, state: FSMContext):
    student_id = await check_student_id(message, state)
    if student_id is None:
        return

    async def reset_data():
        await message.delete()
        await clear_media_group(state)

        await asyncio.sleep(2)

        await state.update_data(
            homework_text_message=None,
            hw_submitted=None,
            last_mgid=None
        )
        await state.set_state()

    hw_date = await state.get_value("hw_date")
    last_mgid = await state.get_value("last_mgid")
    hw_submitted = await state.get_value("hw_submitted")
    feedback_text_message = await state.get_value("feedback_text_message")

    mode = "feedback"

    cur_mgid = message.media_group_id

    if last_mgid is not None and cur_mgid != last_mgid:
        await reset_data()
        return

    if hw_submitted is None:
        hw_submitted = db_utils.set_checked_homework(
            student_id=student_id,
            homework_date=datetime.strptime(hw_date, "%d.%m.%Y")
        )

        await state.update_data(hw_submitted=hw_submitted)

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

    if not hw_submitted:
        await method(
            text=caption,
            reply_markup=kb.BACK_INLINE_KEYBOARD
        )
        await reset_data()
        return

    if message.photo is not None:
        image_path = os.path.join(
            db_utils.IMAGES_PATH.format(student_id, hw_date, mode),
            f"{secrets.token_urlsafe(5)}.png"
        )

        await message.bot.download(
            file=message.photo[-1].file_id,
            destination=image_path
        )

    comment = ""

    if message.caption is not None:
        comment = message.caption
    elif message.text is not None:
        comment = message.text

    with open(
        file=db_utils.COMMENT_PATH.format(student_id, hw_date, mode),
        mode='w',
        encoding="utf-8"
    ) as comment_file:
        comment_file.write(comment)

    try:
        feedback_text_message = await method(
            text=caption,
            reply_markup=kb.BACK_INLINE_KEYBOARD
        )
    except TelegramBadRequest:
        pass
    finally:
        await state.update_data(
            feedback_text_message=feedback_text_message,
            last_mgid=cur_mgid
        )

        await reset_data()


@form_router.callback_query(F.data == "tutor_all_hw")
async def process_get_all_homeworks(callback: CallbackQuery, state: FSMContext):
    student_id = await check_student_id(callback, state)
    if student_id is None:
        return

    await save_last_message(callback.message, state)

    homeworks = db_utils.get_homeworks(student_id=student_id)

    if not homeworks:
        await callback.message.edit_text(
            text=captions.EMPTY,
            reply_markup=kb.BACK_INLINE_KEYBOARD
        )
    else:
        await callback.message.edit_text(
            text=captions.CHOOSE_DATE,
            reply_markup=kb.get_all_homework_inline_keyboard(homeworks)
        )

    await callback.answer()


@form_router.callback_query(F.data.startswith("tutor_check_homework_"))
async def process_select_homework_date(callback: CallbackQuery, state: FSMContext):
    student_id = await check_student_id(callback, state)
    if student_id is None:
        return

    date_str = callback.data.removeprefix("tutor_check_homework_")
    mode = "homework"

    photos = os.listdir(db_utils.IMAGES_PATH.format(student_id, date_str, mode))

    with open(db_utils.COMMENT_PATH.format(student_id, date_str, mode), 'r', encoding='utf-8') as comment_file:
        comment = comment_file.read()

    if not comment:
        comment = captions.EMPTY_TUTOR_COMMENT

    caption = captions.TUTOR_COMMENT.format(comment)

    if photos:
        media_builder = MediaGroupBuilder(caption=caption)
        for photo in photos:
            media_builder.add(
                type="photo",
                media=FSInputFile(os.path.join(
                    db_utils.IMAGES_PATH.format(student_id, date_str, mode),
                    photo)
                )
            )

        media_group = await callback.message.answer_media_group(media=media_builder.build())
        await state.update_data(media_group=media_group)

        await callback.message.answer(
            text=captions.CHOOSE_OPTION,
            reply_markup=kb.BACK_INLINE_KEYBOARD
        )
        await callback.message.delete()
    else:
        await callback.message.edit_text(
            text=caption,
            reply_markup=kb.BACK_INLINE_KEYBOARD
        )

# ======================================================================
# -----------------------------STUDENT BLOCK---------------------------
# ======================================================================

@form_router.callback_query(F.data == "tutor_students")
async def process_tutor_students(callback: CallbackQuery, state: FSMContext):
    await save_last_message(callback.message, state)

    await callback.message.edit_text(
        text=captions.CHOOSE_STUDENT,
        reply_markup=kb.get_students_inline_keyboard()
    )

    await callback.answer()


@form_router.callback_query(F.data.startswith("tutor_select_"))
async def process_select_student(callback: CallbackQuery, state: FSMContext):
    await save_last_message(callback.message, state)

    student_id = callback.data.removeprefix("tutor_select_")
    await state.update_data(student_id=student_id)

    await callback.message.edit_text(
        text=captions.CHOOSE_OPTION,
        reply_markup=kb.TUTOR_OPTION_INLINE_KEYBOARD
    )

    await callback.answer()


@form_router.callback_query(F.data == "tutor_student_options")
async def process_student_options(callback: CallbackQuery, state: FSMContext):
    student_id = await check_student_id(callback.message, state)
    if student_id is None:
        return

    await save_last_message(callback.message, state)

    await callback.message.edit_text(
        text=captions.CHOOSE_OPTION,
        reply_markup=kb.TUTOR_STUDENT_OPTIONS_INLINE_KEYBOARD
    )

    await callback.answer()


#                               ADD / DELETE STUDENT
@form_router.callback_query(F.data == "tutor_add_student")
async def process_add_student(callback: CallbackQuery, state: FSMContext):
    last_msg = await callback.message.edit_text(
        text=captions.SET_STUDENT_TELEGRAM_ID,
        reply_markup=kb.BACK_INLINE_KEYBOARD
    )

    await state.update_data(last_msg=last_msg)
    await state.set_state(TutorForm.setting_student_id)

    await callback.answer()


@form_router.message(TutorForm.setting_student_id)
async def process_set_student_username(message: Message, state: FSMContext):
    student_id = message.text.strip() if message.text is not None else message.caption.strip()
    last_msg = await state.get_value("last_msg")

    method = message.answer if last_msg is None else last_msg.edit_text

    if len(student_id) > 10 or not student_id.isdecimal():
        if last_msg is None or last_msg.text != captions.INCORRECT_TELEGRAM_ID:
            last_msg = await method(
                text=captions.INCORRECT_TELEGRAM_ID,
                reply_markup=kb.BACK_INLINE_KEYBOARD
            )
            await state.update_data(last_msg=last_msg)
    else:
        student_id = int(student_id)
        if db_utils.check_student_exists(telegram_id=student_id):
            await method(
                text=captions.STUDENT_ALREADY_EXISTS,
                reply_markup=kb.BACK_INLINE_KEYBOARD
            )
        else:
            last_msg = await method(
                text=captions.TUTOR_EDIT_STUDENT_NAME,
                reply_markup=None
            )

            await state.set_state(TutorForm.setting_student_name)
            await state.update_data(last_msg=last_msg, student_id=student_id)

    await message.delete()


@form_router.message(TutorForm.setting_student_name)
async def process_set_student_username(message: Message, state: FSMContext):
    last_msg = await state.get_value("last_msg")
    method = message.answer if last_msg is None else last_msg.edit_text

    student_id = await state.get_value("student_id")
    if student_id is None:
        last_msg = await method(
            text=captions.SET_STUDENT_TELEGRAM_ID,
            reply_markup=kb.BACK_INLINE_KEYBOARD
        )
        await state.set_state(TutorForm.setting_student_id)
        await state.update_data(last_msg=last_msg)
        await message.delete()
        return

    name = message.text.strip() if message.text is not None else message.caption.strip()

    if len(name) > 50 or not name.replace(" ", '').isalpha():
        if last_msg is None or last_msg.text != captions.INCORRECT_STUDENT_DATA:
            last_msg = await method(
                text=captions.INCORRECT_STUDENT_DATA,
                reply_markup=kb.BACK_INLINE_KEYBOARD
            )
            await state.update_data(last_msg=last_msg)
    else:
        last_msg = await method(
            text=captions.TUTOR_EDIT_STUDENT_SURNAME,
            reply_markup=None
        )

        await state.set_state(TutorForm.setting_student_surname)
        await state.update_data(last_msg=last_msg, student_name=name)

    await message.delete()


@form_router.message(TutorForm.setting_student_surname)
async def process_set_student_username(message: Message, state: FSMContext):
    last_msg = await state.get_value("last_msg")
    method = message.answer if last_msg is None else last_msg.edit_text

    student_id = await state.get_value("student_id")
    if student_id is None:
        last_msg = await method(
            text=captions.SET_STUDENT_TELEGRAM_ID,
            reply_markup=kb.BACK_INLINE_KEYBOARD
        )
        await state.set_state(TutorForm.setting_student_id)
        await state.update_data(last_msg=last_msg)
        await message.delete()
        return

    name = await state.get_value("student_name")
    if name is None:
        last_msg = await method(
            text=captions.EDIT_STUDENT_NAME,
            reply_markup=kb.BACK_INLINE_KEYBOARD
        )
        await state.set_state(TutorForm.setting_student_name)
        await state.update_data(last_msg=last_msg)
        await message.delete()
        return

    surname = message.text.strip() if message.text is not None else message.caption.strip()

    if len(surname) > 50 or not surname.replace(" ", '').isalpha():
        if last_msg is None or last_msg.text != captions.INCORRECT_STUDENT_DATA:
            last_msg = await method(
                text=captions.INCORRECT_STUDENT_DATA,
                reply_markup=kb.BACK_INLINE_KEYBOARD
            )
            await state.update_data(last_msg=last_msg)
    else:
        await state.set_state()
        await state.update_data(
            student_id=None,
            student_name=None,
            student_surname=None
        )

        student_added = db_utils.add_student(telegram_id=student_id, name=name, surname=surname)

        await method(
            text=(captions.STUDENT_ADD_SUCCESS
                  if student_added
                  else captions.STUDENT_ADD_FAILED),
            reply_markup=kb.BACK_INLINE_KEYBOARD
        )

    await message.delete()


@form_router.callback_query(F.data == "tutor_delete_student")
async def process_delete_student(callback: CallbackQuery, state: FSMContext):
    student_id = await check_student_id(callback.message, state)
    if student_id is None:
        return

    student_deleted = db_utils.delete_student(student_id=student_id)

    if student_deleted:
        await state.update_data(student_id=None)

    await callback.message.edit_text(
        text=(captions.STUDENT_DELETE_SUCCESS if student_deleted else captions.STUDENT_DELETE_FAILED),
        reply_markup=kb.TRIPLE_BACK_INLINE_KEYBOARD
    )

    await callback.answer()


#                               EDIT PROFILE STUDENT
@form_router.callback_query(F.data == "tutor_edit_student_profile")
async def process_student_profile(callback: CallbackQuery, state: FSMContext) -> None:
    student_id = await check_student_id(callback.message, state)
    if student_id is None:
        return

    await save_last_message(callback.message, state)

    student = db_utils.get_student(student_id=student_id)

    name = student.name
    surname = student.surname

    probe_result = student.last_probe_result

    if probe_result is None:
        probe_result = "undefined"

    await callback.message.edit_text(
        text=captions.STUDENT_PROFILE_TEXT.format(
            name, surname, html.code(student_id), probe_result),
        reply_markup=kb.TUTOR_EDIT_STUDENT_PROFILE_INLINE_KEYBOARD
    )

    await callback.answer()


@form_router.callback_query(F.data.startswith("tutor_edit_student_"))
async def process_edit_student_data(callback: CallbackQuery, state: FSMContext) -> None:
    student_id = await check_student_id(callback.message, state)
    if student_id is None:
        return

    await save_last_message(callback.message, state)

    mode = callback.data.removeprefix("tutor_edit_student_")

    if mode is None:
        await callback.message.edit_text(
            text=captions.CHOOSE_OPTION,
            reply_markup=kb.TUTOR_STUDENT_OPTIONS_INLINE_KEYBOARD
        )
    else:
        edit_student_profile_msg = await callback.message.edit_text(
            text=getattr(captions, f"TUTOR_EDIT_STUDENT_{mode.upper()}"),
            reply_markup=kb.BACK_INLINE_KEYBOARD
        )

        await state.update_data(edit_student_profile_msg=edit_student_profile_msg)

    new_state = getattr(TutorForm, f"setting_student_{mode}")
    print(new_state, type(new_state))
    await state.set_state(new_state)

    await callback.answer()


@form_router.message(StateFilter(TutorForm.editing_student_name, TutorForm.editing_student_surname))
async def process_edit_student_name(message: Message, state: FSMContext) -> None:
    student_id = await check_student_id(message, state)
    if student_id is None:
        return

    full_state = await state.get_state()
    mode = full_state.split('_')[-1]

    edit_student_profile_msg = await state.get_value("edit_student_profile_msg")
    new_data = message.text

    updater = getattr(db_utils, f"update_student_{mode}")
    data_updated = updater(new_data, student_id=student_id)

    text = captions.DATA_UPDATED_SUCCESS if data_updated else captions.DATA_UPDATED_FAILED

    await message.delete()
    await state.set_state()

    method = (
        message.answer
        if edit_student_profile_msg is None
        else edit_student_profile_msg.edit_text
    )

    await method(
        text=text,
        reply_markup=kb.DOUBLE_BACK_INLINE_KEYBOARD
    )


@form_router.callback_query(F.data == "tutor_update_probe")
async def process_update_probe(callback: CallbackQuery, state: FSMContext):
    student_id = await check_student_id(callback, state)
    if student_id is None:
        return

    await save_last_message(callback.message, state)

    last_msg = await callback.message.edit_text(
        text=captions.UPDATE_PROBE_RESULT,
        reply_markup=kb.BACK_INLINE_KEYBOARD
    )

    await state.set_state(TutorForm.editing_probe_result)
    await state.update_data(last_msg=last_msg)
    await callback.answer()


@form_router.message(TutorForm.editing_probe_result)
async def process_update_probe_result(message: Message, state: FSMContext):
    student_id = await check_student_id(message, state)
    if student_id is None:
        return

    last_msg = await state.get_value("last_msg")

    method = (
        message.answer
        if last_msg is None
        else last_msg.edit_text
    )

    new_result = message.text
    if new_result.isdecimal() and int(new_result) <= 1000:
        new_result = int(new_result)
        probe_result_updated = db_utils.update_probe_result(new_result, student_id=student_id)

        text = captions.DATA_UPDATED_SUCCESS if probe_result_updated else captions.DATA_UPDATED_FAILED

        await method(
            text=text,
            reply_markup=kb.DOUBLE_BACK_INLINE_KEYBOARD
        )

        await state.set_state()

    else:
        await method(
            text=captions.INCORRECT_FORMAT_RESULT_PROBE,
            reply_markup=kb.DOUBLE_BACK_INLINE_KEYBOARD
        )

    await message.delete()

