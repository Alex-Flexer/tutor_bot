from os import listdir

from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from aiogram.utils.keyboard import InlineKeyboardBuilder


EXAM_TYPE_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="ОГЭ"), KeyboardButton(text="ЕГЭ")]
    ],
    resize_keyboard=True
)

FIRST_CHECKING_STOP_TEST_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Стоп")]],
    resize_keyboard=True
)


FINAL_CHECKING_STOP_TEST_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Стоп"), KeyboardButton(text="Продолжить")]],
    resize_keyboard=True
)


START_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="ОГЭ", callback_data="start_oge"),
         InlineKeyboardButton(text="ЕГЭ", callback_data="start_ege")],
        [InlineKeyboardButton(text="Контакты", callback_data="start_contacts")]
    ]
)

EGE_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="ЕГЭ", callback_data="start_ege")]
    ]
)

OGE_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="ОГЭ", callback_data="start_oge")]
    ]
)

EXAM_TYPE_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="ОГЭ", callback_data="start_oge"),
         InlineKeyboardButton(text="ЕГЭ", callback_data="start_ege")]
    ]
)

MAIN_MENU_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Ученик", callback_data="i_am_student"),
         InlineKeyboardButton(text="Родитель", callback_data="i_am_parent"),
         InlineKeyboardButton(text="Куратор", callback_data="i_am_tutor")],
    ]
)

STUDENT_MENU_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="ЕГЭ/ОГЭ", callback_data="student_exams"),
         InlineKeyboardButton(text="ДЗ", callback_data="student_hw"),
         InlineKeyboardButton(text="Профиль", callback_data="student_profile")]
    ]
)

STUDENT_HW_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Мои задания", callback_data="student_unfinished_hw"),
         InlineKeyboardButton(text="Проверенное ДЗ", callback_data="student_checked_hw"),
         InlineKeyboardButton(text="Сдать на проверку ДЗ", callback_data="student_finish_hw")]
    ]
)

TUTOR_MENU_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="ОГЭ", callback_data="start_oge"),]
    ]
)

PARENT_MENU_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Записаться на урок", callback_data="sign_up_lesson")],
        [InlineKeyboardButton(text="Информация об ученике", callback_data="student_info")]
    ]
)

EXAMS_STUDENT_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Теория", callback_data="student_theory"),
         InlineKeyboardButton(text="Варианты", callback_data="student_variants"),
         InlineKeyboardButton(text="Задания", callback_data="student_tasks")]
    ]
)

THEORY_TYPE_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="По номеру", callback_data="theory_task_number"),
         InlineKeyboardButton(text="По теме", callback_data="theory_topic")]
    ]
)


TASKS_TYPE_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="По номеру", callback_data="tasks_task_number"),
         InlineKeyboardButton(text="По теме", callback_data="tasks_topic")]
    ]
)


def get_theory_topics_inline_keyboard(theory_type: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    topics = [dirname for dirname in listdir(f"./topics/{theory_type}") if dirname.endswith(".txt")]

    for topic in topics:
        builder.button(text=topic, callback_data=f"theory_{theory_type}_{topic}")

    builder.adjust(3, repeat=True)
    return builder.as_markup()


def get_tasks_inline_keyboard(exam_type: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    tasks_number = range([
        task for task in listdir(f"./{exam_type}/0/")
        if task.endswith(".png") and task.rstrip(".png").isdecimal()
    ])

    for task in range(tasks_number):
        builder.button(text=topic, callback_data=f"task_{exam_type}_{task}")

    builder.adjust(4, repeat=True)
    return builder.as_markup()


def get_variants_inline_keyboard(exam_type: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    variants_number = len(listdir(f"./{exam_type}"))

    for var_num in range(variants_number):
        builder.button(text=str(var_num + 1), callback_data=f"variant_{var_num}")

    builder.adjust(4, repeat=True)
    return builder.as_markup()
