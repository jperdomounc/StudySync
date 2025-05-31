"""read up on pydantic documentation"""
"""--pip3 install fast api "uvicorn[standard]"--"""
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import schedule_ranker

app = FastAPI()

class Section(BaseModel):
    start: float
    end: float
    prof_id: str

class ScheduleRequest(BaseModel):
    course_sections: List[List[Section]]
    preferred_range: List[float]
    prof_ratings: dict[str, float]

@app.post("/generate_schedule/")
def generate_schedule(request: ScheduleRequest):
    schedules = generate_schedules(
        schedule_range=tuple(request.preferred_range),
        course_list=[[s.dict() for s in course] for course in request.course_sections],
        prof_ratings=request.prof_ratings
    )
    return {"schedules": schedules}
