from datetime import timedelta
from queue import deque

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup

from utils import captions, keyboards as kb


ENV_PATH = ".env"
CACHE_INTERVAL_EXPIRE = timedelta(days=1)


class TutorForm(StatesGroup):
    inputting_sk = State()
    checking_hw = State()
    updating_probe = State()


class StudentForm(StatesGroup):
    solving_tasks = State()
    uploading_hw = State()
    setting_name = State()
    setting_surname = State()


async def save_last_message(message: Message, state: FSMContext):
    msg_history: deque = await state.get_value("msg_history", deque())

    prev_keyboard = message.reply_markup
    prev_text = message.text

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
