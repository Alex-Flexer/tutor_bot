from datetime import timedelta
from queue import deque

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, CallbackQuery

from utils import captions, keyboards as kb
from database.models import Lesson


ENV_PATH = ".env"
CACHE_INTERVAL_EXPIRE = timedelta(days=1)
EPS_MSG_TIME_INTERVAL = timedelta(seconds=3)


class TutorForm(StatesGroup):
    inputting_sk = State()

    deleting_lesson = State()

    setting_student_id = State()
    setting_student_name = State()
    setting_student_surname = State()

    setting_probe_result = State()

    checking_hw = State()
    uploading_hw = State()

    updating_probe = State()


class StudentForm(StatesGroup):
    solving_tasks = State()
    uploading_hw = State()
    setting_name = State()
    setting_surname = State()


class ParentForm(StatesGroup):
    inputting_student_id = State()
    inputting_email = State()


async def save_last_message(message: Message, state: FSMContext):
    msg_history: deque = await state.get_value("msg_history", deque())

    prev_keyboard = message.reply_markup
    prev_text = message.html_text

    msg_history.append((prev_text, prev_keyboard))

    await state.update_data(msg_history=msg_history)


async def clear_media_group(state: FSMContext):
    media_group = await state.get_value("media_group", [])

    if isinstance(media_group, list):
        for media in media_group:
            if hasattr(media, "delete"):
                await media.delete()
    elif hasattr(media_group, "delete"):
        await media_group.delete()

    await state.update_data(media_group=[])


async def get_previous_message(state: FSMContext) -> tuple[str, InlineKeyboardMarkup]:
    msg_history: deque = await state.get_value("msg_history")

    await clear_media_group(state)

    if not msg_history:
        return (captions.CHOOSE_ROLE, kb.MAIN_MENU_INLINE_KEYBOARD)
    else:
        prev_msg = msg_history.pop()
        await state.update_data(msg_history=msg_history)
        return prev_msg


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


def lessons_to_text(lessons: list[Lesson]) -> str:
    lessons_str = [
        captions.LESSON.format(
            lesson.id,
            lesson.date.strftime("%d.%m.%Y"),
            lesson.email,
            lesson.telegram_username
        )
        for lesson in lessons
    ]

    sep = "\n\n" + "-" * 15 + "\n\n"
    return sep.join(lessons_str)
