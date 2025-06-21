from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from aiogram.utils.keyboard import InlineKeyboardBuilder


BACK_TO_EXAM_TYPE_INLINE_BUTTON = InlineKeyboardButton(
    text="Назад",
    callback_data="back_to_exam_type"
)

BACK_TO_STUDENT_MENU_INLINE_BUTTON = InlineKeyboardButton(
    text="Назад",
    callback_data="back_to_student_menu"
)

BACK_TO_MAIN_MENU_INLINE_BUTTON = InlineKeyboardButton(
    text="Назад",
    callback_data="back_to_main_menu"
)

BACK_TO_STUDENT_HW_INLINE_BUTTON = InlineKeyboardButton(
    text="Назад",
    callback_data="back_to_student_hw"
)

BACK_TO_STUDENT_HW_OPTIONS_INLINE_BUTTON = InlineKeyboardButton(
    text="Назад",
    callback_data="back_to_student_hw_options"
)

BACK_TO_STUDENT_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [BACK_TO_STUDENT_MENU_INLINE_BUTTON]
    ]
)

BACK_TO_STUDENT_HW_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[[BACK_TO_STUDENT_HW_INLINE_BUTTON]]
)

BACK_TO_STUDENT_PROFILE_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="back_to_student_profile")]
    ]
)

BACK_TO_EDIT_STUDENT_PROFILE_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="back_to_edit_student_profile")]
    ]
)

BACK_TO_STUDENT_HW_OPTIONS_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [BACK_TO_STUDENT_HW_OPTIONS_INLINE_BUTTON]
    ]
)

BACK_TO_STUDENT_HW_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [BACK_TO_STUDENT_HW_INLINE_BUTTON]
    ]
)

BACK_TO_HOMEWORK_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="back_to_homework_hw_dates")]
    ]
)

BACK_TO_SUBMIT_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="back_to_submit_hw_dates")]
    ]
)

BACK_TO_FEEDBACK_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="back_to_feedback_hw_dates")]
    ]
)

STOP_TEST_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Стоп", callback_data="test_stop")]],
)


EGE_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="ЕГЭ", callback_data="select_exam_ege")],
        [BACK_TO_EXAM_TYPE_INLINE_BUTTON]
    ]
)

OGE_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="ОГЭ", callback_data="select_exam_oge")],
        [BACK_TO_EXAM_TYPE_INLINE_BUTTON]
    ]
)

EXAM_TYPE_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="ОГЭ", callback_data="select_exam_oge"),
         InlineKeyboardButton(text="ЕГЭ", callback_data="select_exam_ege")],
        [BACK_TO_STUDENT_MENU_INLINE_BUTTON]
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
        [BACK_TO_MAIN_MENU_INLINE_BUTTON]
    ]
)


STUDENT_PROFILE_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Изменить данные", callback_data="edit_student_profile")],
        [BACK_TO_STUDENT_MENU_INLINE_BUTTON]
    ]
)

EDIT_STUDENT_PROFILE_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Имя", callback_data="edit_student_name"),
         InlineKeyboardButton(text="Фамилия", callback_data="edit_student_surname")],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_student_profile")]
    ]
)

STUDENT_HW_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Мои задания", callback_data="student_my_hw"),
         InlineKeyboardButton(text="Сдать на проверку ДЗ", callback_data="student_submit_hw")],
        [BACK_TO_STUDENT_MENU_INLINE_BUTTON]
    ]
)

STUDENT_HW_OPTIONS_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Актуальное", callback_data="student_hw_actual"),
         InlineKeyboardButton(text="Проверенное", callback_data="student_hw_checked")],
        [BACK_TO_STUDENT_HW_INLINE_BUTTON]
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
        [BACK_TO_MAIN_MENU_INLINE_BUTTON]
    ]
)

PREPARATION_TYPE_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Варианты", callback_data="preparation_type_variants"),
         InlineKeyboardButton(text="Задания", callback_data="preparation_type_lines")],
        [BACK_TO_EXAM_TYPE_INLINE_BUTTON]
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
    builder.row(InlineKeyboardButton(text="Назад", callback_data="back_to_preparation_type"))
    return builder.as_markup()


def get_variants_inline_keyboard(variants_number: int = 0) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for var_num in range(variants_number):
        builder.button(text=str(var_num + 1), callback_data=f"variant_{var_num}")

    builder.adjust(4, repeat=True)
    builder.row(InlineKeyboardButton(text="Назад", callback_data="back_to_preparation_type"))
    return builder.as_markup()


def get_homework_dates_inline_keyboard(dates: list[str], mode: str, back_to: InlineKeyboardButton) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for date in dates:
        builder.button(text=date, callback_data=f"homework_{mode}_{date}")

    builder.adjust(4, repeat=True)
    builder.row(back_to)
    return builder.as_markup()
