from aiogram.fsm.state import State, StatesGroup


class TutorForm(StatesGroup):
    inputting_sk = State()

    deleting_lesson = State()

    setting_student_id = State()
    setting_student_name = State()
    setting_student_surname = State()

    setting_probe_result = State()

    checking_hw = State()
    uploading_hw = State()

    updating_probe = State()


class StudentForm(StatesGroup):
    solving_tasks = State()
    uploading_hw = State()
    setting_name = State()
    setting_surname = State()


class ParentForm(StatesGroup):
    inputting_student_id = State()
    inputting_email = State()