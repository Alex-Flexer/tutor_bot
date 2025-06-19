from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import (
    Column, Integer, String, Boolean,
    ForeignKey, DateTime, create_engine,
    UniqueConstraint, CheckConstraint
)


Base = declarative_base()

DB_URL = "sqlite:///database/database.db"


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True)

    email = Column(String(255))
    telegram_username = Column(String(255), nullable=False)
    passed = Column(Boolean, nullable=False, default=False)


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)

    name = Column(String(255), nullable=False)
    surname = Column(String(255), nullable=False)

    telegram_id = Column(Integer, nullable=False, unique=True)
    student_id = Column(String(10), nullable=False, unique=True)

    homeworks = relationship("Homework", back_populates="student")


class Homework(Base):
    __tablename__ = "homeworks"

    id = Column(Integer, primary_key=True)

    student_id = Column(Integer, ForeignKey("students.id"))
    student = relationship("Student", back_populates="homeworks")

    date_setting_homework = Column(DateTime, nullable=False)
    date_submitting_homework = Column(DateTime)

    submitted = Column(Boolean, default=False)
    checked = Column(Boolean, default=False)

    __table_args__ = (
        UniqueConstraint(
            'student_id', 'date_setting_homework',
            name='student_id_date_setting_homework_uc'
        ),
        CheckConstraint(
            'NOT (submitted IS FALSE AND checked IS TRUE)',
            name='check_after_submitted_cc'
        )
    )


engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
Base.metadata.create_all(engine)
