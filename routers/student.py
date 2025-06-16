import json

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    Message,
    ReplyKeyboardRemove,
    FSInputFile,
    CallbackQuery
)

from utils import keyboards, PreparationTypes, ExamTypes


class Form(StatesGroup):
    solving_tasks = State()


with open("answers.json", 'r', encoding='utf-8') as file:
    ANSWERS: dict[str, list[list[str]]] = json.load(file)


form_router = Router()


async def show_results(message: Message, state: FSMContext) -> None:
    text = "Результат:\n\n"

    data = await state.get_data()

    exam_type = data["exam_type"]
    variant_idx = data["variant_idx"]
    task_idx = data["task_idx"]

    if task_idx < 5 and exam_type == ExamTypes.oge:
        task_img = data["task_img"]
        await task_img.delete()

    user_answers: list[str] = data.get("answers", [])
    right_answers: list[str] = ANSWERS[exam_type.value][variant_idx]

    cnt_right_solutions = 0

    for idx, (user_answer, right_answer) in enumerate(zip(user_answers, right_answers)):
        verdict = user_answer.replace(".", ",").replace(" ", "") == right_answer
        cnt_right_solutions += verdict
        text += f"{idx + 1}) {"+" if verdict else "-"}\n"

    text += f"\nВаш результат: {cnt_right_solutions}/{len(user_answers)}"

    if cnt_right_solutions == len(right_answers):
        photo = FSInputFile("./images/perfect_img.jpg")
        await message.answer_photo(
            photo,
            text,
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        await message.answer(text, reply_markup=ReplyKeyboardRemove())

    await message.answer(
        "Хотите продолжить подготовку?",
        reply_markup=(
            keyboards.EXAM_TYPE_INLINE_KEYBOARD if len(user_answers) != len(right_answers)
            else (
                keyboards.EGE_INLINE_KEYBOARD
                if exam_type == ExamTypes.oge
                else keyboards.OGE_INLINE_KEYBOARD)
        )
    )


async def show_task(message: Message, state: FSMContext) -> None:
    data = await state.get_data()

    # preparation_type = data["preparation_type"]
    exam_type = data["exam_type"]
    task_idx = data["task_idx"]
    variant_idx = data["variant_idx"]

    # add dependence on preparation type

    photo_path = join(".", exam_type.value, str(variant_idx), str(task_idx) + ".png")
    photo = FSInputFile(photo_path)
    caption = f"ЗАДАНИЕ №{task_idx + 1}"

    if task_idx > 0:
        last_msg = data["last_msg"]
        await last_msg.delete()

    if task_idx == 5 and exam_type == ExamTypes.oge:
        task_img = data["task_img"]
        await task_img.delete()

    last_msg = await message.answer_photo(
        photo,
        caption=caption,
        reply_markup=keyboards.STOP_TEST_INLINE_KEYBOARD
    )
    await state.update_data(last_msg=last_msg)


@form_router.callback_query(F.data.contains("student_exams"))
async def command_solve(message: Message, state: FSMContext) -> None:
    await message.answer(
        "Выберите тип экзамена:",
        reply_markup=keyboards.EXAM_TYPE_INLINE_KEYBOARD,
    )


@form_router.callback_query(F.data.startswith("start_"))
async def process_exam_choice(callback: CallbackQuery, state: FSMContext) -> None:
    exam_type = (
        ExamTypes.ege
        if callback.data.lstrip("start_") == ExamTypes.ege.value
        else ExamTypes.oge
    )

    await state.update_data(exam_type=exam_type)

    await callback.message.edit_text(
        f"Выберите вид подготовки:",
        reply_markup=keyboards.PREPARATION_TYPE_INLINE_KEYBOARD
    )

    await callback.answer()


@form_router.callback_query(F.data.startswith("student_exam"))
async def command_solve_1(callback: CallbackQuery, state: FSMContext) -> None:
    preparation_type = (
        PreparationTypes.variants
        if callback.data.lstrip("student_exam_") == "variants"
        else PreparationTypes.tasks
    )

    exam_type = await state.get_value("exam_type")

    new_keyboard, new_text = (
        keyboards.get_variants_inline_keyboard(exam_type.value), "Выберите номер варианта:"
        if preparation_type == PreparationTypes.variants
        else keyboards.get_tasks_inline_keyboard(exam_type.value), "Выберите номер задания:"
    )

    await callback.message.edit_reply_markup(reply_markup=new_keyboard)
    await callback.message.edit_text(new_text)

    await state.update_data(preparation_type=preparation_type)

    await callback.answer()


@form_router.callback_query(F.data.startswith("variant_"))
async def process_variant_number(callback: CallbackQuery, state: FSMContext) -> None:
    variant_number = int(callback.data.lstrip("variant_"))
    message = callback.message

    exam_type = await state.get_value("exam_type")

    variant_idx = variant_number - 1

    await state.update_data(
        variant_idx=variant_idx,
        task_idx=0,
        answers=[]
    )

    await state.set_state(Form.solving_tasks)
    await message.answer(f"ВАРИАНТ №{variant_number}", reply_markup=ReplyKeyboardRemove())

    if exam_type == ExamTypes.oge:
        task_img = await message.answer_photo(FSInputFile(f"./oge/{variant_idx}/img.png"))
        await state.update_data(task_img=task_img)

    await show_task(message, state)

    callback.answer()


@form_router.callback_query(F.data.startswith("task_"))
async def process_task_number(callback: CallbackQuery, state: FSMContext) -> None:
    task_number = int(callback.data.lstrip("variant_"))
    message = callback.message

    exam_type = await state.get_value("exam_type")
    line_idx = task_number - 1

    await state.update_data(
        line_idx=line_idx,
        task_idx=0,
        answers=[]
    )

    await state.set_state(Form.solving_tasks)
    await message.answer(f"НОМЕР №{task_number}", reply_markup=ReplyKeyboardRemove())

    # if exam_type == ExamTypes.oge:
    #     task_img = await message.answer_photo(FSInputFile(f"./oge/{line_idx}/img.png"))
    #     await state.update_data(task_img=task_img)

    # await show_task(message, state)

    callback.answer()


@form_router.message(Form.solving_tasks)
async def process_answer_task(message: Message, state: FSMContext) -> None:
    data = await state.get_data()

    exam_type = data["exam_type"]

    answer = message.text
    answers = data.get("answers", []) + [answer]

    task_idx = data["task_idx"] + 1
    variant_idx = data["variant_idx"]
    await state.update_data(answers=answers, task_idx=task_idx)

    max_tasks = len(listdir(join(".", exam_type.value, str(variant_idx)))) - \
        (exam_type == ExamTypes.oge)

    if task_idx == max_tasks:
        await show_results(message, state)
        await state.set_state(None)
        await state.update_data(
            answers=[],
            task_idx=None,
            variant_idx=None
        )
    else:
        await message.delete()
        await show_task(message, state)


@form_router.callback_query(Form.solving_tasks, F.data.contains("test_stop"))
async def process_stop_final(callback: CallbackQuery, state: FSMContext) -> None:
    if await state.get_value("variant_idx") is not None:
        await show_results(callback.message, state)
    else:
        await callback.message.answer(
            "Тест приостановлен.",
            reply_markup=keyboards.EXAM_TYPE_INLINE_KEYBOARD
        )

    await state.set_state(None)
    await state.update_data(answers=[], task_idx=None, variant_idx=None, task_img=None)
    await callback.answer()
