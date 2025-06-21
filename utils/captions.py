from utils import keyboards
from aiogram import html


HELLO_TEXT = """👋 Привет!
Ты в умном боте для подготовки к ЕГЭ и ОГЭ математике.

Здесь ты сможешь:
✅ Проверить свои ответы.
✅ Получишь консультацию через кнопку «контакты»

🚀 Просто выберете номер варианта и отправь свой ответ — бот всё проверит!
И помни: каждая ошибка — это шаг к 100 баллам.

Готов проверить себя? Погнали! 🎯
"""


CONTACTS_TEXT = """Поддержка:

Присоединяйтесь к нашему Telegram-каналу:
@matnas7

💬 Если у вас есть вопросы или вам нужна помощь:
@NikitaAlekseevichh"""

CHOOSE_ROLE = "Кем вы являетесь?"

CHOOSE_OPTION = "Выберете одну из представленный ниже опций:"

YOUR_RESULT_NO_DATA = "Результат:"

YOUR_RESULT = "Ваш результат: {}/{}"

RESULT_LINE = "{}) {}\n"

TASK_NUMBER = "ЗАДАНИЕ №{}"

LINE_NUMBER = "НОМЕР №{}"

VARIANT_NUMBER = "ВАРИАНТ №{}"

AKS_CONTINUE = "Хотите продолжить подготовку?"

TEST_STOPPED = "Тест приостановлен."

CHOOSE_EXAM_TYPE = "Выберите тип экзамена:"

CHOOSE_PREPARATION_TYPE = "Выберите вид подготовки:"

CHOOSE_VARIANT_NUMBER = "Выберите номер варианта:"

CHOOSE_LINE_NUMBER = "Выберите номер задания:"

CHOOSE_TASKS_NUMBER = "Выберте число заданий:"

STUDENT_NOT_FOUND = "Пользователь не найден. Обратитесь в опддержку для решения проблемы."

CHOOSE_DATE = "Выберете дату задания:"

EMPTY = "Здесь пока ничего нет."

SUBMIT_HOMEWORK = f"""{html.bold("Важно:")}

Принимаются {html.bold("только фото с текстом")} в сообщении, файлы и прочите форматы будут проигнорированы

Домашнее задание нужно отправить {html.bold("одним сообщением")}, все последующие сообщения будут также проигнорированы

Домашнее задание {html.bold("позже будет нельзя отправить")} занаво или редактировать

Отправьте домашнее задание:"""

TUTOR_COMMENT = "Комментарий куратора: \n\n{}"

EMPTY_TUTOR_COMMENT = "Куратор не оставил комментария."

HW_SUBMITTED_SUCCESS = "Домашнее задание успешно отправлено."

HW_SUBMITTED_FAILED = "Домашнее задание не было отправлено. Обратитесь в опддержку для решения проблемы."

EDIT_STUDENT_PROFILE = "Выберете данные для изменения:"

EDIT_STUDENT_NAME = "Введите ваше имя:"

EDIT_STUDENT_SURNAME = "Введите вашу фамилию:"

DATA_UPDATED_SUCCESS = "Данные успешно обновлены."

DATA_UPDATED_FAILED = "Не удалось обновить данные. Обратитесь в поддержку для решения проблемы."

PROFILE_TEXT = """Ваш профиль:

Имя: {}
Фамилия: {}
StudentID: {}
"""

UNKNOWN_COMMAND = "Неизвестная команда."

keyboard2captions = {
    keyboards.MAIN_MENU_INLINE_KEYBOARD: CHOOSE_ROLE,
    keyboards.STUDENT_MENU_INLINE_KEYBOARD: CHOOSE_OPTION,
    keyboards.EXAM_TYPE_INLINE_KEYBOARD: CHOOSE_EXAM_TYPE,
    keyboards.EGE_INLINE_KEYBOARD: AKS_CONTINUE,
    keyboards.OGE_INLINE_KEYBOARD: AKS_CONTINUE,
    keyboards.PREPARATION_TYPE_INLINE_KEYBOARD: CHOOSE_PREPARATION_TYPE,
    keyboards.get_variants_inline_keyboard(): CHOOSE_VARIANT_NUMBER,
    keyboards.TASKS_NUMBER_INLINE_KEYBOARD: CHOOSE_TASKS_NUMBER,
    keyboards.STUDENT_HW_INLINE_KEYBOARD: CHOOSE_OPTION,
    keyboards.STUDENT_HW_OPTIONS_INLINE_KEYBOARD: CHOOSE_OPTION,
    keyboards.STUDENT_PROFILE_INLINE_KEYBOARD: PROFILE_TEXT,
    keyboards.EDIT_STUDENT_PROFILE_INLINE_KEYBOARD: EDIT_STUDENT_PROFILE
}
