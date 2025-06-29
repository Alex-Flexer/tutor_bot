from queue import deque

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, CallbackQuery

from utils import captions, keyboards as kb
from database.models import Lesson


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


async def get_previous_message(state: FSMContext, k=1) -> tuple[str, InlineKeyboardMarkup]:
    msg_history: deque = await state.get_value("msg_history")
    
    if not msg_history:
        return (captions.CHOOSE_ROLE, kb.MAIN_MENU_INLINE_KEYBOARD)

    await clear_media_group(state)
    await state.set_state()
    
    for _ in range(k - 1):
        if len(msg_history) == 1:
            break
        msg_history.pop()

    prev_msg = (
        msg_history.pop()
        if len(msg_history) > 1
        else msg_history[0]
    )
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


async def check_value_empty(method, state: FSMContext, key: str, text: str, keyboard: InlineKeyboardMarkup):
    student_id = await state.get_value(key)
    if student_id is None:
        last_msg = await method(
            text=text,
            reply_markup=keyboard
        )
        await state.update_data(last_msg=last_msg)
    return student_id
        


def lessons_to_text(lessons: list[Lesson]) -> str:
    lessons_str = [
        (captions.LESSON_EMAIL.format(
            lesson.id,
            lesson.date.strftime("%d.%m.%Y"),
            lesson.email,
            lesson.telegram_username
        )
        if lesson.email is not None
        else
        captions.LESSON_OTHER_DATA.format(
            lesson.id,
            lesson.date.strftime("%d.%m.%Y"),
            lesson.other_data,
            lesson.telegram_username
        ))
        for lesson in lessons
    ]

    sep = "\n\n" + "-" * 15 + "\n\n"
    return sep.join(lessons_str)
