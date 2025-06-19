import json
import random
import os

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.types import (
    Message,
    ReplyKeyboardRemove,
    FSInputFile,
    CallbackQuery,
    InputMediaPhoto
)

from utils import keyboards, captions, PreparationTypes, ExamTypes
from database import utils as db_utils


def get_tasks_number(exam_type: ExamTypes, variant_idx: int = 0) -> int:
    return sum(
        1 for filename in os.listdir(os.path.join(".", exam_type.value, str(variant_idx)))
        if filename.endswith(".png") and filename.rstrip(".png").isdecimal()
    )


def get_variants_number(exam_type: ExamTypes) -> int:
    return sum(
        1 for dirname in os.listdir(os.path.join(".", exam_type.value))
        if dirname.isdecimal()
    )


for exam_type in ExamTypes:
    variants_number = get_variants_number(exam_type)
    random_tasks_number = get_tasks_number(exam_type, random.randint(0, variants_number - 1))

    assert (
        all(
            get_tasks_number(exam_type, variant_number) == random_tasks_number
            for variant_number in range(variants_number)
        )
    ), f"Tasks number must be the same in all variants of {exam_type.value.upper()}"


with open("answers.json", 'r', encoding='utf-8') as file:
    ANSWERS: dict[str, list[list[str]]] = json.load(file)


class Form(StatesGroup):
    solving_tasks = State()


form_router = Router()


async def show_results(message: Message, state: FSMContext) -> None:
    text = captions.YOUR_RESULT_NO_DATA + "\n\n"

    data = await state.get_data()

    preparation_type = data["preparation_type"]
    exam_type = data["exam_type"]

    task_idx = data["task_idx"]if preparation_type == PreparationTypes.variants else data["line_idx"]

    if task_idx < 5 and exam_type == ExamTypes.oge:
        task_img = data["task_img"]
        await task_img.delete()

    student_answers: list[str] = data.get("answers", [])

    right_answers: list[str] = (
        ANSWERS[exam_type.value][data["variant_idx"]]
        if preparation_type == PreparationTypes.variants
        else
        [ANSWERS[exam_type.value][variant_idx][task_idx] for variant_idx in data["variants"]]
    )

    cnt_right_solutions = 0

    for idx, (user_answer, right_answer) in enumerate(zip(student_answers, right_answers)):
        verdict = user_answer.replace(".", ",").replace(" ", "") == right_answer
        cnt_right_solutions += verdict

        text += captions.RESULT_LINE.format(idx + 1, "+" if verdict else "-")

    text += "\n" + captions.YOUR_RESULT.format(cnt_right_solutions, len(student_answers))

    if cnt_right_solutions == len(right_answers):
        photo = FSInputFile("./images/perfect_img.jpg")
        await message.answer_photo(
            photo=photo,
            caption=text,
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        await message.answer(text, reply_markup=ReplyKeyboardRemove())

    await message.answer(
        text=captions.AKS_CONTINUE,
        reply_markup=(
            keyboards.EXAM_TYPE_INLINE_KEYBOARD if len(student_answers) != len(right_answers)
            else (
                keyboards.EGE_INLINE_KEYBOARD
                if exam_type == ExamTypes.ege
                else keyboards.OGE_INLINE_KEYBOARD)
        )
    )


async def show_variant_task(message: Message, state: FSMContext) -> None:
    data = await state.get_data()

    exam_type = data["exam_type"]
    task_idx = data["task_idx"]
    variant_idx = data["variant_idx"]

    photo_path = os.path.join(".", exam_type.value, str(variant_idx), str(task_idx) + ".png")
    photo = FSInputFile(photo_path)
    caption = captions.TASK_NUMBER.format(task_idx + 1)

    if task_idx > 0:
        last_msg = data["last_msg"]
        await last_msg.delete()

    if exam_type == ExamTypes.oge:

        if task_idx == 0:
            task_img = await message.answer_photo(FSInputFile(f"./oge/{variant_idx}/img.png"))
            await state.update_data(task_img=task_img)

        elif task_idx == 5:
            task_img = data["task_img"]
            await task_img.delete()

    last_msg = await message.answer_photo(
        photo=photo,
        caption=caption,
        reply_markup=keyboards.STOP_TEST_INLINE_KEYBOARD
    )

    await state.update_data(last_msg=last_msg)


async def show_line_task(message: Message, state: FSMContext) -> None:
    data = await state.get_data()

    exam_type = data["exam_type"]
    line_idx = data["line_idx"]
    task_idx = data["task_idx"]
    variants = data["variants"]

    variant_idx = variants[task_idx]

    photo_path = os.path.join(".", exam_type.value, str(variant_idx), str(line_idx) + ".png")

    print(photo_path)

    photo = FSInputFile(photo_path)
    caption = captions.TASK_NUMBER.format(task_idx + 1)

    if exam_type == ExamTypes.oge and line_idx < 5 and task_idx == 0:
        task_img = await message.answer_photo(FSInputFile(f"./oge/{variant_idx}/img.png"))
        await state.update_data(task_img=task_img)

    if task_idx == 0:
        last_msg = await message.answer_photo(
            photo=photo,
            caption=caption,
            reply_markup=keyboards.STOP_TEST_INLINE_KEYBOARD
        )
    else:
        last_msg = data["last_msg"]

        if exam_type == ExamTypes.oge and line_idx < 5:
            task_img = data["task_img"]
            await task_img.edit_media(
                media=InputMediaPhoto(media=FSInputFile(f"./oge/{variant_idx}/img.png"))
            )

        last_msg = await last_msg.edit_media(
            InputMediaPhoto(media=photo, caption=caption),
            reply_markup=keyboards.STOP_TEST_INLINE_KEYBOARD
        )

    await state.update_data(last_msg=last_msg)


async def show_task(message: Message, state: FSMContext) -> None:
    if await state.get_value("preparation_type") == PreparationTypes.variants:
        await show_variant_task(message, state)
    else:
        await show_line_task(message, state)


@form_router.callback_query(F.data == "student_exams")
async def process_student_exams(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        text=captions.CHOOSE_EXAM_TYPE,
        reply_markup=keyboards.EXAM_TYPE_INLINE_KEYBOARD
    )


@form_router.callback_query(F.data == "student_hw")
async def process_student_hw(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        text=captions.CHOOSE_OPTION,
        reply_markup=keyboards.STUDENT_HW_INLINE_KEYBOARD
    )


@form_router.callback_query(F.data == "student_my_hw")
async def process_student_my_hw(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        text=captions.CHOOSE_OPTION,
        reply_markup=keyboards.STUDENT_HW_OPTIONS_INLINE_KEYBOARD
    )


@form_router.callback_query(F.data.in_(("student_hw_checked", "student_hw_actual")))
async def process_student_hw_checked(callback: CallbackQuery) -> None:
    mode = callback.data.removeprefix("student_hw_") == "checked"
    print(mode)

    telegram_id = callback.from_user.id
    homeworks = db_utils.get_homeworks(telegram_id=telegram_id, checked=mode, submitted=mode)

    if not homeworks:
        print(homeworks)
        if homeworks is None:
            name = callback.from_user.first_name
            surname = callback.from_user.last_name

            db_utils.add_student(name, surname, telegram_id)

        await callback.message.edit_text(
            text=captions.EMPTY,
            reply_markup=keyboards.BACK_TO_STUDENT_HW_INLINE_KEYBOARD
        )
    else:
        dates = db_utils.homeworks_to_str_dates(homeworks)

        await callback.message.edit_text(
            text=captions.CHOOSE_HOMEWORK_DATE,
            reply_markup=keyboards.get_homework_dates_inline_keyboard(dates, "checked" if mode else "homework")
        )


@form_router.callback_query(F.data.startswith("homework_"))
async def process_student_homework(callback: CallbackQuery) -> None:
    mode, date = callback.data.removeprefix("homework_").split("_")
    telegram_id = callback.from_user.id
    print(mode, date, telegram_id, callback.data.removeprefix("homework_").split("_"), callback.data)

    student = db_utils.get_student(telegram_id=telegram_id)
    student_id = student.student_id

    photos = os.listdir(db_utils.IMAGES_PATH.format(student_id, date, mode))

    with open(db_utils.COMMENT_PATH.format(student_id, date, mode), 'r', encoding='utf-8') as comment_file:
        comment = comment_file.read()

    caption = captions.TUTOR_COMMENT.format(comment) if comment else captions.EMPTY_TUTOR_COMMENT

    media_builder = MediaGroupBuilder(caption=caption)

    for photo in photos:
        media_builder.add(
            type="photo",
            media=FSInputFile(os.path.join(db_utils.IMAGES_PATH.format(student_id, date, mode), photo))
        )

    await callback.message.answer_media_group(media=media_builder.build())

    await callback.answer()


@form_router.callback_query(F.data.startswith("start_"))
async def process_exam_choice(callback: CallbackQuery, state: FSMContext) -> None:
    exam_type = (
        ExamTypes.ege
        if callback.data.removeprefix("start_") == ExamTypes.ege.value
        else ExamTypes.oge
    )

    await state.update_data(exam_type=exam_type)

    await callback.message.edit_text(
        text=captions.CHOOSE_PREPARATION_TYPE,
        reply_markup=keyboards.PREPARATION_TYPE_INLINE_KEYBOARD
    )

    await callback.answer()


@form_router.callback_query(F.data.startswith("student_exam_"))
async def process_preparation_type(callback: CallbackQuery, state: FSMContext) -> None:
    preparation_type = PreparationTypes[callback.data.removeprefix("student_exam_")]

    exam_type = await state.get_value("exam_type")

    new_keyboard, new_text = (
        (
            keyboards.get_variants_inline_keyboard(get_variants_number(exam_type)),
            captions.CHOOSE_VARIANT_NUMBER
        )
        if preparation_type == PreparationTypes.variants
        else (
            keyboards.get_lines_inline_keyboard(get_tasks_number(exam_type)),
            captions.CHOOSE_TASK_NUMBER
        )
    )

    await callback.message.edit_text(new_text, reply_markup=new_keyboard)

    await state.update_data(preparation_type=preparation_type)

    await callback.answer()


@form_router.callback_query(F.data.startswith("variant_"))
async def process_variant_number(callback: CallbackQuery, state: FSMContext) -> None:
    variant_idx = int(callback.data.removeprefix("variant_"))
    message = callback.message

    await state.update_data(
        task_idx=0,
        variant_idx=variant_idx,
        answers=[]
    )

    await state.set_state(Form.solving_tasks)
    await message.answer(f"ВАРИАНТ №{variant_idx}", reply_markup=ReplyKeyboardRemove())

    await show_variant_task(message, state)

    await callback.answer()


@form_router.callback_query(F.data.startswith("line_"))
async def process_line_number(callback: CallbackQuery, state: FSMContext) -> None:
    line_idx = int(callback.data.removeprefix("line_"))
    await state.update_data(line_idx=line_idx)

    await callback.message.edit_text(
        text=captions.CHOOSE_TASKS_NUMBER,
        reply_markup=keyboards.TASKS_NUMBER_INLINE_KEYBOARD
    )

    await callback.answer()


@form_router.callback_query(F.data.startswith("tasks_"))
async def process_tasks_number(callback: CallbackQuery, state: FSMContext) -> None:
    tasks_number = int(callback.data.removeprefix("tasks_"))
    line_idx = await state.get_value("line_idx")

    message = callback.message

    exam_type = await state.get_value("exam_type")

    await state.update_data(
        task_idx=0,
        variants=random.choices(range(get_variants_number(exam_type)), k=tasks_number),
        answers=[]
    )

    await state.set_state(Form.solving_tasks)
    await message.answer(
        text=captions.LINE_NUMBER.format(line_idx + 1),
        reply_markup=ReplyKeyboardRemove()
    )

    await show_task(message, state)
    await callback.answer()


@form_router.message(Form.solving_tasks)
async def process_answer_task(message: Message, state: FSMContext) -> None:
    data = await state.get_data()

    exam_type = data["exam_type"]
    preparation_type = data["preparation_type"]

    answer = message.text
    answers = data.get("answers", []) + [answer]

    task_idx = data["task_idx"] + 1

    await state.update_data(answers=answers, task_idx=task_idx)

    max_tasks = (
        len(data["variants"])
        if preparation_type == PreparationTypes.lines
        else get_tasks_number(exam_type, data["variant_idx"])
    )

    await message.delete()

    if task_idx == max_tasks:
        await data["last_msg"].delete()
        await show_results(message, state)

        await state.clear()
        await state.update_data(answers=[])

    else:
        await show_task(message, state)


@form_router.callback_query(Form.solving_tasks, F.data.contains("test_stop"))
async def process_stop(callback: CallbackQuery, state: FSMContext) -> None:
    if await state.get_value("variant_idx") is not None:
        await show_results(callback.message, state)
    else:
        await callback.message.answer(
            text=captions.TEST_STOPPED,
            reply_markup=keyboards.EXAM_TYPE_INLINE_KEYBOARD
        )

    await state.clear()
    await state.update_data(answers=[])

    await callback.answer()


@form_router.callback_query(F.data.startswith("back_to_"))
async def process_back_to(callback: CallbackQuery, state: FSMContext) -> None:
    exam_type = await state.get_value("exam_type")
    previous_keyboard_name = callback.data.removeprefix("back_to_").upper()
    print(previous_keyboard_name)

    if exam_type is None and previous_keyboard_name == "LINE":
        text, keyboard = (
            (
                captions.CHOOSE_OPTION,
                keyboards.STUDENT_MENU_INLINE_KEYBOARD
            )
            if callback.message.reply_markup.dict() == keyboards.EXAM_TYPE_INLINE_KEYBOARD.dict()
            else (
                captions.CHOOSE_EXAM_TYPE,
                keyboards.EXAM_TYPE_INLINE_KEYBOARD
            )
        )
    elif previous_keyboard_name == "ACTUAL_HW_DATES":
        text = captions.CHOOSE_OPTION
        # keyboard = ...
    else:
        keyboard, text = (
            (
                keyboards.get_lines_inline_keyboard(get_tasks_number(exam_type)),
                captions.CHOOSE_PREPARATION_TYPE
            )
            if previous_keyboard_name == "LINE"
            else (
                (tmp_keyboard := getattr(keyboards, f"{previous_keyboard_name}_INLINE_KEYBOARD")),
                captions.keyboard2captions[tmp_keyboard]
            )
        )

    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard
    )

    await callback.answer()
