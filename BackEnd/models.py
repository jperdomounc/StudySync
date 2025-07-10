"""pydantic models"""
from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import datetime

class SchedulePreferences(BaseModel):
    earliest_time: str  # "08:00"
    latest_time: str    # "18:00"

class ShoppingCart(BaseModel):
    pasted_text: str
    preferences: SchedulePreferences

class Course(BaseModel):
    title: str
    instructor: str
    days: List[str]
    start_time: str
    end_time: str
    rating: Optional[float]

class NoteCreate(BaseModel):
    title: str
    content: str
    course: Optional[str] = ""
    tags: List[str] = []
    
    @validator('title')
    def validate_title(cls, v):
        if not v.strip():
            raise ValueError('Title cannot be empty')
        if len(v) > 100:
            raise ValueError('Title too long (max 100 characters)')
        return v.strip()
    
    @validator('content')
    def validate_content(cls, v):
        if not v.strip():
            raise ValueError('Content cannot be empty')
        if len(v) > 5000:
            raise ValueError('Content too long (max 5000 characters)')
        return v.strip()
    
    @validator('course')
    def validate_course(cls, v):
        if v and len(v) > 50:
            raise ValueError('Course name too long (max 50 characters)')
        return v.strip() if v else ""
    
    @validator('tags')
    def validate_tags(cls, v):
        if len(v) > 10:
            raise ValueError('Too many tags (max 10)')
        validated_tags = []
        for tag in v:
            tag = tag.strip()
            if tag:
                if len(tag) > 30:
                    raise ValueError('Tag too long (max 30 characters)')
                validated_tags.append(tag)
        return validated_tags

class Note(BaseModel):
    id: int
    title: str
    content: str
    course: str
    tags: List[str]
    created_at: datetime
