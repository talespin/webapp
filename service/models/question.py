from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from app.db import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)

    exam_year = Column(Integer, nullable=False)
    exam_name = Column(String(100), nullable=False)
    subject = Column(String(50), nullable=False)
    section = Column(String(50), nullable=False)

    question_number = Column(Integer, nullable=False)
    score = Column(Integer)
    question_type = Column(String(50))

    question_text = Column(Text, nullable=False)
    choices = Column(JSONB)
    answer = Column(String(50))
    solution_text = Column(Text)

    difficulty_score = Column(Float)
    difficulty_label = Column(String(50))

    curriculum_subject = Column(String(100))
    curriculum_unit = Column(String(100))

    created_at = Column(DateTime(timezone=True), server_default=func.now())
