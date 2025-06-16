from os import listdir

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from aiogram.utils.keyboard import InlineKeyboardBuilder


_BACK_BUTTON = InlineKeyboardButton(text="Назад", callback_data="back")


STOP_TEST_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Стоп", callback_data="test_stop")]],
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
         InlineKeyboardButton(text="ЕГЭ", callback_data="start_ege")],
        [_BACK_BUTTON]
    ]
)

MAIN_MENU_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Ученик", callback_data="i_am_student"),
         InlineKeyboardButton(text="Родитель", callback_data="i_am_parent"),
         InlineKeyboardButton(text="Куратор", callback_data="i_am_tutor")]
    ]
)

STUDENT_MENU_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="ЕГЭ/ОГЭ", callback_data="student_exams"),
         InlineKeyboardButton(text="ДЗ", callback_data="student_hw"),
         InlineKeyboardButton(text="Профиль", callback_data="student_profile")],
        [_BACK_BUTTON]
    ]
)

STUDENT_HW_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Мои задания", callback_data="student_hw_unfinished"),
         InlineKeyboardButton(text="Проверенное ДЗ", callback_data="student_hw_checked"),
         InlineKeyboardButton(text="Сдать на проверку ДЗ", callback_data="student_hw_finish")],
        [_BACK_BUTTON]
    ]
)

TUTOR_MENU_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Проверить ДЗ", callback_data="tutor_check_hw"),]
    ]
)

PARENT_MENU_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Записаться на урок", callback_data="parent_sign_up_lesson")],
        [InlineKeyboardButton(text="Информация об ученике", callback_data="parent_student_info")],
        [_BACK_BUTTON]
    ]
)

PREPARATION_TYPE_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Варианты", callback_data="student_exam_variants"),
         InlineKeyboardButton(text="Задания", callback_data="student_exam_tasks")],
        [_BACK_BUTTON]
    ]
)


def get_tasks_inline_keyboard(exam_type: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    tasks_number = range([
        task for task in listdir(f"./{exam_type}/0/")
        if task.endswith(".png") and task.rstrip(".png").isdecimal()
    ])

    for task in range(tasks_number):
        builder.button(text=task, callback_data=f"task_{task}")

    builder.adjust(4, repeat=True)
    builder.button(_BACK_BUTTON)
    return builder.as_markup()


def get_variants_inline_keyboard(exam_type: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    variants_number = len(listdir(f"./{exam_type}"))

    for var_num in range(variants_number):
        builder.button(text=str(var_num + 1), callback_data=f"variant_{var_num}")

    builder.adjust(4, repeat=True)
    builder.button(_BACK_BUTTON)
    return builder.as_markup()
