"""read up on pydantic documentation"""
"""--pip3 install fast api "uvicorn[standard]"--"""
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class ClassInfo(BaseModel):
    course_name: str
    professor_name: str
    start_time: str  
    end_time: str   
    rating: Optional[float] = None  # for later RMP API

@app.get("/")
def root():
    return {"message": "StudySync"}, {"classes": sample_classes}

@app.post("/generate_schedule/")
def generate_schedule(classes: List[ClassInfo]):
    # to do 
    return {
        "message": "Generated schedule!",
        "schedule": classes
    }

sample_classes = {0: ClassInfo("COMP110", "Dr. Berzatto", "8:00", "9:15")}

# http://127.0.0.1:8000