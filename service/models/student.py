from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func

from db import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100))
    target_grade = Column(Integer)
    target_percentile = Column(Float)

    created_at = Column(DateTime(timezone=True), server_default=func.now())


class StudentAnswer(Base):
    __tablename__ = "student_answers"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)

    is_correct = Column(Boolean, nullable=False)
    selected_answer = Column(String(50))
    time_spent_seconds = Column(Integer)

    solved_at = Column(DateTime(timezone=True), server_default=func.now())


class StudentConceptMastery(Base):
    __tablename__ = "student_concept_mastery"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    concept_id = Column(Integer, ForeignKey("concepts.id"), nullable=False)

    mastery_score = Column(Float, default=0.5)
    confidence = Column(Float, default=0.0)

    last_updated = Column(DateTime(timezone=True), server_default=func.now())
