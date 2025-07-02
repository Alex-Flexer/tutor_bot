from datetime import datetime, timedelta

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from aiogram.utils.keyboard import InlineKeyboardBuilder

from database import utils as db_utils



# ======================================================================
# ----------------------------COMMON BLOCK------------------------------
# ======================================================================

MAIN_MENU_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Ученик", callback_data="i_am_student"),
         InlineKeyboardButton(text="Родитель", callback_data="i_am_parent")]
    ]
)

BACK_INLINE_BUTTON = InlineKeyboardButton(text="Назад", callback_data="back_1")

BACK_INLINE_KEYBOARD = InlineKeyboardMarkup(inline_keyboard=[[BACK_INLINE_BUTTON]])

DOUBLE_BACK_INLINE_KEYBOARD = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Назад", callback_data="back_2")]])

TRIPLE_BACK_INLINE_KEYBOARD = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Назад", callback_data="back_3")]])

# ======================================================================
# ----------------------------STUDENT BLOCK-----------------------------
# ======================================================================

CONTACTS_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Контакты", url="https://t.me/NikitaAlekseevichh")]],
)

STOP_TEST_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Стоп", callback_data="test_stop")]],
)


EGE_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="ЕГЭ", callback_data="select_exam_ege")],
        [BACK_INLINE_BUTTON]
    ]
)

OGE_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="ОГЭ", callback_data="select_exam_oge")],
        [BACK_INLINE_BUTTON]
    ]
)

EXAM_TYPE_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="ОГЭ", callback_data="select_exam_oge"),
         InlineKeyboardButton(text="ЕГЭ", callback_data="select_exam_ege")],
        [BACK_INLINE_BUTTON]
    ]
)

STUDENT_MENU_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="ЕГЭ/ОГЭ", callback_data="student_exams"),
         InlineKeyboardButton(text="ДЗ", callback_data="student_hw"),
         InlineKeyboardButton(text="Профиль", callback_data="student_profile")],
        [InlineKeyboardButton(text="ИИ-ассистент", callback_data="start_ai_chatting")],
        [BACK_INLINE_BUTTON]
    ]
)

STUDENT_PROFILE_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Изменить данные", callback_data="edit_student_profile")],
        [BACK_INLINE_BUTTON]
    ]
)

EDIT_STUDENT_PROFILE_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Имя", callback_data="edit_student_name"),
         InlineKeyboardButton(text="Фамилия", callback_data="edit_student_surname")],
        [BACK_INLINE_BUTTON]
    ]
)

STUDENT_HW_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Мои задания", callback_data="student_my_hw"),
         InlineKeyboardButton(text="Сдать на проверку ДЗ", callback_data="student_submit_hw")],
        [BACK_INLINE_BUTTON]
    ]
)

STUDENT_HW_OPTIONS_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Актуальное", callback_data="student_hw_actual"),
         InlineKeyboardButton(text="Проверенное", callback_data="student_hw_checked")],
        [BACK_INLINE_BUTTON]
    ]
)

PREPARATION_TYPE_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Варианты", callback_data="preparation_type_variants"),
         InlineKeyboardButton(text="Задания", callback_data="preparation_type_lines")],
        [BACK_INLINE_BUTTON]
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
        [BACK_INLINE_BUTTON]
    ]
)

STOP_CHATTING = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Стоп", callback_data="stop_ai_chatting")]
    ]
)

def get_lines_inline_keyboard(tasks_number: int = 0) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for task in range(tasks_number):
        builder.button(text=str(task + 1), callback_data=f"line_{task}")

    builder.adjust(4, repeat=True)
    builder.row(BACK_INLINE_BUTTON)
    return builder.as_markup()


def get_variants_inline_keyboard(variants_number: int = 0) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for var_num in range(variants_number):
        builder.button(text=str(var_num + 1), callback_data=f"variant_{var_num}")

    builder.adjust(4, repeat=True)
    builder.row(BACK_INLINE_BUTTON)
    return builder.as_markup()


def get_homework_dates_inline_keyboard(dates: list[str], mode: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for date in dates:
        builder.button(text=date, callback_data=f"homework_{mode}_{date}")

    builder.adjust(4, repeat=True)
    builder.row(BACK_INLINE_BUTTON)
    return builder.as_markup()

# ======================================================================
# ------------------------------TUTOR BLOCK-----------------------------
# ======================================================================

TUTOR_MENU_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Ученики", callback_data="tutor_students"),
         InlineKeyboardButton(text="Записи", callback_data="tutor_lessons")]
    ]
)

TUTOR_OPTION_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="ДЗ", callback_data="tutor_hw"),
         InlineKeyboardButton(text="Ученик", callback_data="tutor_student_options")],
        [BACK_INLINE_BUTTON]
    ]
)

TUTOR_SET_HW_STATUS_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Хорошо", callback_data="tutor_set_hw_status_good"),
         InlineKeyboardButton(text="Плохо", callback_data="tutor_set_hw_status_bad")],
        [BACK_INLINE_BUTTON]
    ]
)

TUTOR_STUDENT_OPTIONS_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Удалить ученика", callback_data="tutor_delete_student")],
        [InlineKeyboardButton(text="Редактировать профиль ученика", callback_data="tutor_edit_student_profile")],
        [BACK_INLINE_BUTTON]
    ]
)

TUTOR_HW_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Проверить", callback_data="tutor_check_hw"),
         InlineKeyboardButton(text="Задать", callback_data="tutor_set_hw")],
        [InlineKeyboardButton(text="Все", callback_data="tutor_all_hw")],
        [BACK_INLINE_BUTTON]
    ]
)

TUTOR_EDIT_STUDENT_PROFILE_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Имя", callback_data="tutor_edit_student_name"),
         InlineKeyboardButton(text="Фамилия", callback_data="tutor_edit_student_surname")],
        [InlineKeyboardButton(text="Обновить результаты пробника", callback_data="tutor_update_probe")],
        [InlineKeyboardButton(text="Изменить ссылку на GoogleDisk", callback_data="tutor_edit_student_gd_link")],
        [BACK_INLINE_BUTTON]
    ]
)



def get_students_inline_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for students_id in db_utils.get_all_students():
        builder.button(text=students_id, callback_data=f"tutor_select_{students_id}")

    builder.adjust(4, repeat=True)

    builder.row(
        InlineKeyboardButton(
            text="Добавить ученика",
            callback_data="tutor_add_student"
        )
    )
    builder.row(BACK_INLINE_BUTTON)
    return builder.as_markup()


def get_dates_in_month_inline_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    today = datetime.today()
    for i in range(30):
        date_str = (today + timedelta(days=i)).strftime("%d.%m.%Y")
        builder.button(text=date_str, callback_data=f"tutor_set_hw_{date_str}")

    builder.adjust(5, repeat=True)
    builder.row(BACK_INLINE_BUTTON)

    return builder.as_markup()


def get_all_homework_inline_keyboard(homeworks: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for hw in homeworks:
        date_str = hw.date_setting_homework.strftime("%d.%m.%Y")
        builder.button(text=date_str, callback_data=f"tutor_check_homework_{date_str}")

    builder.adjust(5, repeat=True)
    builder.row(BACK_INLINE_BUTTON)

    return builder.as_markup()

# ======================================================================
# -----------------------------PARENT BLOCK-----------------------------
# ======================================================================


PARENT_MENU_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Записаться на урок", callback_data="parent_sign_up_lesson")],
        [InlineKeyboardButton(text="Информация об ученике", callback_data="parent_student_info")],
        [BACK_INLINE_BUTTON]
    ]
)

ADD_LESSON_INLINE_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Другой способ записи на урок", callback_data="another_way_sign_up_lesson")],
        [BACK_INLINE_BUTTON]
    ]
)
