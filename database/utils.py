from datetime import datetime, time
import secrets
import os
import shutil

from sqlalchemy.orm import Session

from .models import Lesson, Student, Homework, engine


_BASIC_HOMEWORK_PATH = "./database/homeworks"

_HOMEWORK_STUDENT_DATE_PATH = _BASIC_HOMEWORK_PATH + "/{}/{}"
_STUDENT_HOMEWORK_PATH = _BASIC_HOMEWORK_PATH + "/{}"

_HOMEWORK_STUDENT_DATE_MODE_PATH = _BASIC_HOMEWORK_PATH + "/{}/{}/{}"
_HOMEWORK_STUDENT_DATE_MODE_IMAGES_PATH = _HOMEWORK_STUDENT_DATE_MODE_PATH + "/images"

IMAGES_PATH = _HOMEWORK_STUDENT_DATE_MODE_IMAGES_PATH
COMMENT_PATH = _HOMEWORK_STUDENT_DATE_MODE_PATH + "/comment.txt"


def _post_commit(func):
    def wrapper(*args, **kwargs):
        with Session(engine) as session:
            res = func(session, *args, **kwargs)
            session.commit()
        return res
    return wrapper


def _catch_except(exc=Exception, default=False):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                res = func(*args, **kwargs)
            except exc as e:
                print(e)
                return default
            else:
                return res
        return wrapper
    return decorator


def _auto_session(func):
    def wrapper(*args, **kwargs):
        with Session(engine) as session:
            return func(session, *args, **kwargs)
    return wrapper


@_catch_except()
@_post_commit
def add_lesson(session: Session, telegram_username: str, email: str = None, other_data=None) -> bool:
    if not ((email is None) ^ (other_data is None)):
        return False

    date = datetime.combine(datetime.today(), time.min)

    amount_lessons_today = len(
        session.query(Lesson).filter(
            Lesson.telegram_username == telegram_username,
            Lesson.date == date
        ).all()
    )

    if amount_lessons_today >= 3:
        return False

    if email is not None:
        session.add(Lesson(email=email, telegram_username=telegram_username, date=date))
    else:
        session.add(Lesson(other_data=other_data, telegram_username=telegram_username, date=date))

    return True


@_catch_except()
@_post_commit
def add_student(session: Session, telegram_id: int, gd_link: str, name: str | None = None, surname: str | None = None) -> bool:
    name = "undefined" if name is None else name
    surname = "undefined" if surname is None else surname

    student_id = secrets.token_urlsafe(2) + str(telegram_id % 10000) + secrets.token_urlsafe(3)
    session.add(Student(
        name=name,
        surname=surname,
        telegram_id=telegram_id,
        student_id=student_id,
        gd_link=gd_link
    )
    )
    return True


@_catch_except()
@_post_commit
def delete_student(session: Session, student_id: str) -> bool:
    student = get_student(student_id=student_id)
    if student is not None:
        session.query(Homework).filter_by(student_id=student.id).delete()

        student_dir_path = _STUDENT_HOMEWORK_PATH.format(student_id)
        if os.path.exists(student_dir_path):
            shutil.rmtree(student_dir_path)

        session.query(Student).filter_by(student_id=student_id).delete()

    return True


@_catch_except()
@_post_commit
def delete_lesson(session: Session, lesson_id) -> None:
    session.query(Lesson).filter_by(id=lesson_id).delete()
    return True


@_catch_except()
@_post_commit
def set_homework(session: Session, student_id: str, homework_date: datetime) -> bool:
    student = get_student(student_id=student_id)
    if student is None:
        return False

    homework_date = datetime.combine(homework_date.date(), time.min)
    homework_date_str = homework_date.date().strftime("%d.%m.%Y")

    session.add(Homework(
        student_id=student.id,
        date_setting_homework=homework_date
    ))

    if not os.path.exists(_BASIC_HOMEWORK_PATH):
        os.mkdir(_BASIC_HOMEWORK_PATH)

    if not os.path.exists(_STUDENT_HOMEWORK_PATH.format(student_id)):
        os.mkdir(_STUDENT_HOMEWORK_PATH.format(student_id))

    if not os.path.exists(_HOMEWORK_STUDENT_DATE_PATH.format(student_id, homework_date_str)):
        os.mkdir(_HOMEWORK_STUDENT_DATE_PATH.format(student_id, homework_date_str))

        for mode in ("homework", "feedback", "submitted"):
            os.mkdir(_HOMEWORK_STUDENT_DATE_MODE_PATH.format(student_id, homework_date_str, mode))
            os.mkdir(_HOMEWORK_STUDENT_DATE_MODE_IMAGES_PATH.format(
                student_id, homework_date_str, mode))
            open(
                file=COMMENT_PATH.format(student_id, homework_date_str, mode),
                mode='x',
                encoding='utf-8'
            ).close()

    return True


@_catch_except()
@_post_commit
def set_submitted_homework(session: Session, student_id: str, homework_date: datetime) -> bool:
    if not check_student_exists(student_id=student_id):
        return False

    student_id = get_student(student_id=student_id).id

    homework_date = datetime.combine(homework_date.date(), time.min)

    homework = session\
        .query(Homework)\
        .filter_by(
            student_id=student_id,
            date_setting_homework=homework_date
        ).first()

    if homework is None:
        return False

    homework.submitted = True
    return True


@_catch_except()
@_post_commit
def set_checked_homework(session: Session, student_id: str, homework_date: datetime, passed: bool) -> bool:
    if not check_student_exists(student_id=student_id):
        print("iii")
        return False

    student_id = get_student(student_id=student_id).id

    homework_date = datetime.combine(homework_date.date(), time.min)

    homework = session\
        .query(Homework)\
        .filter_by(
            student_id=student_id,
            date_setting_homework=homework_date,
        ).first()

    if homework is None:
        print("ppppppp")
        return False

    homework.passed = passed
    homework.checked = True
    return True


@_catch_except()
@_auto_session
def get_last_checked_homeworks(session: Session, k=3, **kwargs) -> list[Homework] | None:
    student = _get_student(session, **kwargs)
    if student is None:
        return None

    return sorted(
        [hw for hw in student.homeworks if hw.checked],
        key=lambda hw: hw.date_setting_homework,
        reverse=True
    )[:k]
    print("good")


@_auto_session
def get_student(session: Session, **kwargs) -> Student | None:
    return session.query(Student).filter_by(**kwargs).first()


@_auto_session
def get_homework(session: Session, student_id: str, date: datetime) -> Homework | None:
    student = get_student(student_id=student_id)
    return session.query(Homework).filter_by(student_id=student.id, date_setting_homework=date).first()


def _get_student(session: Session, **kwargs) -> Student | None:
    return session.query(Student).filter_by(**kwargs).first()


@_catch_except()
@_post_commit
def update_student_data(session: Session, key: str, value: str | int, **kwargs) -> bool | None:
    student = _get_student(session, **kwargs)
    if student is None:
        return None

    session.query(Student).update({key: value})
    return True


def check_student_exists(**kwargs) -> bool:
    return get_student(**kwargs) is not None


@_auto_session
def get_unpassed_lessons(session: Session) -> list[Lesson] | None:
    return session.query(Lesson).filter_by(passed=False).all()


@_auto_session
def get_all_students(session: Session) -> list[Student]:
    return [student.student_id for student in session.query(Student).all()]


@_auto_session
def get_lessons(session: Session) -> list[Lesson]:
    return session.query(Lesson).all()


def get_student_probe_result(**kwargs) -> int | None:
    return get_student(**kwargs).last_probe_result


@_catch_except(default=[])
@_auto_session
def get_homeworks(
    session: Session,
    submitted: bool | None = None,
    checked: bool | None = None,
    **kwargs
) -> list[Homework] | None:

    student = get_student(**kwargs)
    if student is None:
        return None

    sub_kwargs = {}

    if submitted is not None:
        sub_kwargs.update(submitted=submitted)

    if checked is not None:
        sub_kwargs.update(checked=checked)

    return session\
        .query(Homework)\
        .filter_by(
            student_id=student.id,
            **sub_kwargs
        ).all()


def homeworks_to_str_dates(homeworks: list[Homework]) -> list[str]:
    return [hw.date_setting_homework.date().strftime("%d.%m.%Y") for hw in homeworks]


def check_hw_exists(student_id: str, homework_date: datetime) -> bool:
    homeworks: list[Homework] | None = get_homeworks(student_id=student_id)
    if homeworks is None:
        return False

    return any(homework_date == hw.date_setting_homework for hw in homeworks)
