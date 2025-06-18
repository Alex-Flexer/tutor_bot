from os import listdir

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from aiogram.utils.keyboard import InlineKeyboardBuilder



STOP_TEST_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Стоп", callback_data="test_stop")]],
)


EGE_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="ЕГЭ", callback_data="start_ege")],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_exam_type")]
    ]
)

OGE_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="ОГЭ", callback_data="start_oge")],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_exam_type")]
    ]
)

EXAM_TYPE_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="ОГЭ", callback_data="start_oge"),
         InlineKeyboardButton(text="ЕГЭ", callback_data="start_ege")],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_student_menu")]
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
        [InlineKeyboardButton(text="Назад", callback_data="back_to_main_menu")]
    ]
)

STUDENT_BACK_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="back_to_student_menu")]
    ]
)

STUDENT_HW_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Мои задания", callback_data="student_hw_unfinished"),
         InlineKeyboardButton(text="Проверенное ДЗ", callback_data="student_hw_checked"),
         InlineKeyboardButton(text="Сдать на проверку ДЗ", callback_data="student_hw_finish")],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_student_menu")]
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
        [InlineKeyboardButton(text="Назад", callback_data="back_to_main_menu")]
    ]
)

PREPARATION_TYPE_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Варианты", callback_data="student_exam_variants"),
         InlineKeyboardButton(text="Задания", callback_data="student_exam_lines")],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_exam_type")]
    ]
)

TASKS_NUMBER_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=str(tasks_number),
                callback_data=f"tasks_{tasks_number}"
            )
            for tasks_number in (3, 5, 10, 15)
        ],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_line")]
    ]
)


def get_lines_inline_keyboard(tasks_number: int = 0) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for task in range(tasks_number):
        builder.button(text=str(task + 1), callback_data=f"line_{task}")

    builder.adjust(4, repeat=True)
    builder.button(text="Назад", callback_data="back_to_preparation_type")
    return builder.as_markup()


def get_variants_inline_keyboard(variants_number: int = 0) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for var_num in range(variants_number):
        builder.button(text=str(var_num + 1), callback_data=f"variant_{var_num}")

    builder.adjust(4, repeat=True)
    builder.button(text="Назад", callback_data="back_to_preparation_type")
    return builder.as_markup()
