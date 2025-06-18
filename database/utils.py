from datetime import datetime
import secrets
import os

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from .models import Lesson, Student, Homework, engine


BASIC_HOMEWORK_PATH = "./database/homeworks"
HOMEWORK_STUDENT_DATE_HOMEWORK_PATH = BASIC_HOMEWORK_PATH + "/{}/{}/homework"
HOMEWORK_STUDENT_DATE_SUBMITTED_PATH = BASIC_HOMEWORK_PATH + "/{}/{}/submitted"
HOMEWORK_STUDENT_DATE_PATH = BASIC_HOMEWORK_PATH + "/{}/{}"
STUDENT_HOMEWORK_PATH = BASIC_HOMEWORK_PATH + "/{}"


def post_commit(func):
    def wrapper(*args, **kwargs):
        with Session(engine) as session:
            res = func(session, *args, **kwargs)
            session.commit()
        return res
    return wrapper


def catch_except(exc=IntegrityError):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                res = func(*args, **kwargs)
            except exc:
                return False
            else:
                return res
        return wrapper
    return decorator


def auto_session(func):
    def wrapper(*args, **kwargs):
        with Session(engine) as session:
            return func(session, *args, **kwargs)
    return wrapper


@catch_except()
@post_commit
def add_lesson(session: Session, email: str, telegram_username: str) -> bool:
    session.add(Lesson(email, telegram_username, False))
    return True

@catch_except()
@post_commit
def pass_lesson(session: Session, email: str, telegram_username: str) -> bool:
    session.add(Lesson(email, telegram_username, False))
    return True


@catch_except()
@post_commit
def add_student(session: Session, name: str, surname: str, telegram_id: int) -> bool:
    student_id = secrets.token_urlsafe(2) + str(telegram_id % 100) + secrets.token_urlsafe(3)
    session.add(Student(
        name=name,
        surname=surname,
        telegram_id=telegram_id,
        student_id=student_id)
    )
    return True


@catch_except()
@post_commit
def set_homework(session: Session, student_id: str) -> bool:
    if not check_student_exists(student_id):
        return False

    today = datetime.now().date()
    today_str = today.strftime("%d.%m.%Y")

    if not os.path.exists(BASIC_HOMEWORK_PATH):
        os.mkdir(BASIC_HOMEWORK_PATH)

    if not os.path.exists(STUDENT_HOMEWORK_PATH.format(student_id)):
        os.mkdir(STUDENT_HOMEWORK_PATH.format(student_id))

    if os.path.exists(HOMEWORK_STUDENT_DATE_PATH.format(student_id, today_str)):
        return False

    os.mkdir(HOMEWORK_STUDENT_DATE_PATH.format(student_id, today_str))
    os.mkdir(HOMEWORK_STUDENT_DATE_HOMEWORK_PATH.format(student_id, today_str))
    os.mkdir(HOMEWORK_STUDENT_DATE_SUBMITTED_PATH.format(student_id, today_str))

    session.add(Homework(
        student_id=student_id,
        date_setting_homework=today
    ))
    return True


@auto_session
def get_student_by_telegram_id(session: Session, telegram_id: int) -> Student | None:
    return session.query(Student).filter_by(telegram_id=telegram_id).first()


@auto_session
def get_student_by_student_id(session: Session, student_id: int) -> Student | None:
    return session.query(Student).filter_by(student_id=student_id).first()


@auto_session
def check_student_exists(session: Session, student_id: str) -> bool:
    return get_student_by_student_id(student_id) is not None


@auto_session
def get_unpassed_lessons(session: Session) -> list[Lesson] | None:
    return session.query(Lesson).filter_by(passed=False).all()
