from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func

from app.db import Base


class ConceptPrerequisite(Base):
    __tablename__ = "concept_prerequisites"

    id = Column(Integer, primary_key=True, index=True)

    prerequisite_concept_id = Column(Integer, ForeignKey("concepts.id", ondelete="CASCADE"), nullable=False, index=True)
    target_concept_id = Column(Integer, ForeignKey("concepts.id", ondelete="CASCADE"), nullable=False, index=True)

    relation_type = Column(String(50), nullable=False, default="prerequisite")
    strength = Column(Float, nullable=False, default=1.0)
    explanation = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class QuestionLink(Base):
    __tablename__ = "question_links"

    id = Column(Integer, primary_key=True, index=True)

    source_question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True)
    target_question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False, index=True)

    relation_type = Column(String(50), nullable=False)
    strength = Column(Float, nullable=False, default=1.0)
    explanation = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
