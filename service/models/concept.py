from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey

from db import Base


class Concept(Base):
    __tablename__ = "concepts"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)
    subject = Column(String(50), nullable=False)

    parent_concept_id = Column(Integer, ForeignKey("concepts.id"), nullable=True)

    curriculum_subject = Column(String(100))
    curriculum_unit = Column(String(100))
    description = Column(Text)


class QuestionConcept(Base):
    __tablename__ = "question_concepts"

    id = Column(Integer, primary_key=True, index=True)

    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    concept_id = Column(Integer, ForeignKey("concepts.id"), nullable=False)

    role = Column(String(50))
    weight = Column(Float, default=1.0)
