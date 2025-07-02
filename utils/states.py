from aiogram.fsm.state import State, StatesGroup


class TutorForm(StatesGroup):
    deleting_lesson = State()

    setting_student_id = State()
    setting_student_name = State()
    setting_student_surname = State()
    setting_student_gd_link = State()

    editing_student_name = State()
    editing_student_surname = State()
    editing_probe_result = State()
    editing_student_gd_link = State()

    checking_hw = State()
    uploading_hw = State()


class StudentForm(StatesGroup):
    solving_tasks = State()
    uploading_hw = State()

    setting_name = State()
    setting_surname = State()
    
    ai_chatting = State()


class ParentForm(StatesGroup):
    inputting_student_id = State()
    inputting_email = State()
    inputting_other_data = State()
