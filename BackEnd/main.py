from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel
from models import ShoppingCart, Course, NoteCreate, Note
from parser import parse_shopping_cart
from optimizer import ScheduleOptimizer
from notes_db import notes_db

app = FastAPI()
optimizer = ScheduleOptimizer()

# Allow frontend on localhost to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class OptimizedScheduleResponse(BaseModel):
    schedules: List[List[Course]]
    total_found: int

class AddCourseRequest(BaseModel):
    existing_schedule: List[Course]
    new_course_title: str
    available_courses: List[Course]

@app.post("/generate_schedule", response_model=List[Course])
def generate_schedule(cart: ShoppingCart):
    # Parse raw shopping cart text into structured courses
    all_courses = parse_shopping_cart(cart.pasted_text)
    
    # Filter by time preferences (optional but useful)
    filtered = [
        c for c in all_courses
        if cart.preferences.earliest_time <= c.start_time <= cart.preferences.latest_time
    ]

    return filtered

@app.post("/optimize_schedule", response_model=OptimizedScheduleResponse)
def optimize_schedule(cart: ShoppingCart):
    """Generate optimized schedules based on professor ratings"""
    # Parse raw shopping cart text into structured courses
    all_courses = parse_shopping_cart(cart.pasted_text)
    
    # Filter by time preferences
    filtered = [
        c for c in all_courses
        if cart.preferences.earliest_time <= c.start_time <= cart.preferences.latest_time
    ]
    
    # Add professor ratings to courses
    for course in filtered:
        course.rating = optimizer.get_professor_rating(course.instructor)
    
    # Generate optimized schedules
    optimized_schedules = optimizer.optimize_schedule(filtered, max_schedules=5)
    
    return OptimizedScheduleResponse(
        schedules=optimized_schedules,
        total_found=len(optimized_schedules)
    )

@app.post("/add_course_to_schedule", response_model=List[Course])
def add_course_to_schedule(request: AddCourseRequest):
    """Find a schedule that fits an additional course"""
    new_schedule = optimizer.find_schedule_with_additional_course(
        request.existing_schedule,
        request.new_course_title,
        request.available_courses
    )
    
    # Update ratings for the new schedule
    for course in new_schedule:
        course.rating = optimizer.get_professor_rating(course.instructor)
    
    return new_schedule

# Notes API endpoints
@app.post("/notes", response_model=Note)
def create_note(note_data: NoteCreate):
    """Create a new note with safety validations"""
    try:
        note = notes_db.create_note(note_data)
        return note
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to create note")

@app.get("/notes", response_model=List[Note])
def get_all_notes():
    """Get all notes"""
    try:
        return notes_db.get_all_notes()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve notes")

@app.get("/notes/{note_id}", response_model=Note)
def get_note(note_id: int):
    """Get a specific note by ID"""
    note = notes_db.get_note_by_id(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    """Delete a note by ID"""
    success = notes_db.delete_note(note_id)
    if not success:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"message": "Note deleted successfully"}

@app.get("/notes/course/{course}", response_model=List[Note])
def get_notes_by_course(course: str):
    """Get all notes for a specific course"""
    try:
        return notes_db.get_notes_by_course(course)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve course notes")
