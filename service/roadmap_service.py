from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy import text, select
from typing import Optional, List, Dict, Any

from db import get_db_conn, sql_loader
from service.models.concept import Concept
from service.models.student import Student, StudentConceptMastery

class RoadmapService:
    STATIC_UNITS = [
        # 국어
        ("국어", "문학", "현대시"),
        ("국어", "문학", "고전시가"),
        ("국어", "문학", "현대소설"),
        ("국어", "문학", "고전소설"),
        ("국어", "독서", "인문"),
        ("국어", "독서", "사회"),
        ("국어", "독서", "과학기술"),
        ("국어", "언어와 매체", "문법 개념"),
        ("국어", "화법과 작문", "화법"),
        ("국어", "화법과 작문", "작문"),

        # 영어
        ("영어", "독해", "주제/제목"),
        ("영어", "독해", "빈칸 추론"),
        ("영어", "독해", "순서 배열"),
        ("영어", "독해", "문장 삽입"),
        ("영어", "독해", "어휘"),
        ("영어", "독해", "문법"),
        ("영어", "듣기", "대화 내용"),
        ("영어", "듣기", "세부 정보"),

        # 탐구 예시
        ("탐구", "사회탐구", "사회문화 개념"),
        ("탐구", "사회탐구", "경제 도표"),
        ("탐구", "과학탐구", "생명과학 유전"),
        ("탐구", "과학탐구", "화학 양적관계"),
        ("탐구", "과학탐구", "물리 역학"),
        ("탐구", "과학탐구", "지구과학 천체"),
    ]
    def __init__(self, conn: AsyncConnection = Depends(get_db_conn)):
        self.conn = conn

    @staticmethod
    def level_from_mastery(score: float):
        if score is None:
            return 0
        if score < 0.2:
            return 1
        if score < 0.4:
            return 2
        if score < 0.65:
            return 3
        if score < 0.85:
            return 4
        return 5


    async def get_curriculum_roadmap(self, student_id: int):
        query = select(Student).where(Student.id == student_id)
        result = await self.conn.execute(query)
        student = result.scalar_one_or_none()        
        return student

        if student is None:
            raise HTTPException(status_code=404, detail="Student not found")

        mastery_rows = (
            await self.conn.execute(StudentConceptMastery)
            .filter(StudentConceptMastery.student_id == student_id)
            .all()
        )

        mastery_by_concept_id = {
            row.concept_id: row.mastery_score
            for row in mastery_rows
        }

        units = []

        math_concepts = (
            await self.conn.execute(Concept)
            .filter(Concept.subject == "math")
            .order_by(Concept.id.asc())
            .all()
        )

        for concept in math_concepts:
            mastery = mastery_by_concept_id.get(concept.id, 0.0)

            units.append(
                {
                    "unit_id": f"math-{concept.id}",
                    "concept_id": concept.id,
                    "subject": "수학",
                    "area": concept.curriculum_unit or "수학",
                    "unit_name": concept.name,
                    "mastery_score": round(float(mastery), 4),
                    "level": level_from_mastery(float(mastery)),
                    "solved_count": 0,
                    "wrong_count": 0,
                    "source": "concept_mastery",
                }
            )

        for idx, (subject, area, unit_name) in enumerate(STATIC_UNITS, start=1):
            units.append(
                {
                    "unit_id": f"static-{idx}",
                    "concept_id": None,
                    "subject": subject,
                    "area": area,
                    "unit_name": unit_name,
                    "mastery_score": 0.0,
                    "level": 0,
                    "solved_count": 0,
                    "wrong_count": 0,
                    "source": "static",
                }
            )

        by_subject = {}

        for unit in units:
            by_subject.setdefault(unit["subject"], []).append(unit)

        subject_summaries = []

        for subject, items in by_subject.items():
            avg = sum(item["mastery_score"] for item in items) / len(items) if items else 0.0
            subject_summaries.append(
                {
                    "subject": subject,
                    "unit_count": len(items),
                    "average_mastery": round(avg, 4),
                    "completed_units": sum(1 for item in items if item["mastery_score"] >= 0.8),
                }
            )

        overall_avg = sum(unit["mastery_score"] for unit in units) / len(units) if units else 0.0

        return {
            "student_id": student_id,
            "student_name": student.name,
            "overall_mastery": round(overall_avg, 4),
            "total_units": len(units),
            "subject_summaries": subject_summaries,
            "units": units,
        }