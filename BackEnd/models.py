"""pydantic models"""
from pydantic import BaseModel
from typing import List, Optional

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
