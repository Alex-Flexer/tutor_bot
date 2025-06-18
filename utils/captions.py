from utils import keyboards


YOUR_RESULT_NO_DATA = "Результат:"

YOUR_RESULT = "Ваш результат: {}/{}"

RESULT_LINE = "{}) {}\n"

AKS_CONTINUE = "Хотите продолжить подготовку?"

TASK_NUMBER = "ЗАДАНИЕ №{}"

LINE_NUMBER = "НОМЕР №{}"

TEST_STOPPED = "Тест приостановлен."

CHOOSE_EXAM_TYPE = "Выберите тип экзамена:"

CHOOSE_PREPARATION_TYPE = "Выберите вид подготовки:"

CHOOSE_VARIANT_NUMBER = "Выберите номер варианта:"

CHOOSE_TASK_NUMBER = "Выберите номер задания:"

CHOOSE_TASKS_NUMBER = "Выберте число заданий:"

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

UNKNOWN_COMMAND = "Неизвестная команда."

keyboard2captions = {
    keyboards.MAIN_MENU_INLINE_KEYBOARD: CHOOSE_ROLE,
    keyboards.STUDENT_MENU_INLINE_KEYBOARD: CHOOSE_OPTION,
    keyboards.EXAM_TYPE_INLINE_KEYBOARD: CHOOSE_EXAM_TYPE,
    keyboards.EGE_INLINE_KEYBOARD: AKS_CONTINUE,
    keyboards.OGE_INLINE_KEYBOARD: AKS_CONTINUE,
    keyboards.PREPARATION_TYPE_INLINE_KEYBOARD: CHOOSE_PREPARATION_TYPE,
    keyboards.get_variants_inline_keyboard(): CHOOSE_VARIANT_NUMBER,
    keyboards.TASKS_NUMBER_INLINE_KEYBOARD: CHOOSE_TASKS_NUMBER
}
