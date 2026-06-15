from fastapi import APIRouter, Depends, HTTPException, status
from service.roadmap_service import RoadmapService

router = APIRouter(
    prefix='/api/roadmap',
)


@router.get("/students/{student_id}/curriculum-roadmap")
async def get_curriculum_roadmap(student_id: int, roadmap_service: RoadmapService = Depends(RoadmapService)):
    roadmap_service = await roadmap_service.get_curriculum_roadmap(student_id)
    return {
        #"student_id": student_id,
        #"student_name": student.name,
        #"overall_mastery": round(overall_avg, 4),
        #"total_units": len(units),
        #"subject_summaries": subject_summaries,
        #"units": units,
    }

