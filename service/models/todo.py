from sqlalchemy import Boolean, Column, Date, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func

from app.db import Base


class StudyTodo(Base):
    __tablename__ = "study_todos"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True)
    due_date = Column(Date, nullable=False, index=True)

    title = Column(Text, nullable=False)
    description = Column(Text, nullable=True)

    category = Column(String(50), nullable=False, default="study")
    source_type = Column(String(50), nullable=True)
    source_id = Column(Integer, nullable=True)

    priority = Column(Float, nullable=False, default=50.0)
    is_done = Column(Boolean, nullable=False, default=False)

    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class TodoSubject(Base):
    __tablename__ = "todo_subjects"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    color = Column(String(20), nullable=False, default="#6f7cff")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
