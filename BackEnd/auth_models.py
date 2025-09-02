"""Authentication and user management models"""
from pydantic import BaseModel, validator, Field
from typing import List, Optional
from datetime import datetime
import re

class UserCreate(BaseModel):
    email: str
    password: str
    major: str
    grad_year: int
    
    @validator('email')
    def validate_unc_email(cls, v):
        if not v:
            raise ValueError('Email is required')
        
        # Check if it's a UNC email
        unc_pattern = r'^[a-zA-Z0-9._%+-]+@(unc\.edu|live\.unc\.edu|ad\.unc\.edu)$'
        if not re.match(unc_pattern, v.lower()):
            raise ValueError('Must use a valid UNC email address (@unc.edu, @live.unc.edu, or @ad.unc.edu)')
        
        return v.lower()
    
    @validator('password')
    def validate_password(cls, v):
        if not v:
            raise ValueError('Password is required')
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if len(v) > 100:
            raise ValueError('Password too long (max 100 characters)')
        # Check for at least one letter and one number
        if not re.search(r'[A-Za-z]', v) or not re.search(r'\d', v):
            raise ValueError('Password must contain at least one letter and one number')
        return v
    
    @validator('major')
    def validate_major(cls, v):
        if not v.strip():
            raise ValueError('Major is required')
        if len(v) > 100:
            raise ValueError('Major name too long (max 100 characters)')
        return v.strip()
    
    @validator('grad_year')
    def validate_grad_year(cls, v):
        current_year = datetime.now().year
        if v < current_year or v > current_year + 10:
            raise ValueError(f'Graduation year must be between {current_year} and {current_year + 10}')
        return v

class User(BaseModel):
    id: Optional[str] = None
    email: str
    major: str
    grad_year: int
    display_name: str
    created_at: datetime
    is_active: bool = True

class LoginRequest(BaseModel):
    email: str
    password: str
    
    @validator('email')
    def validate_email(cls, v):
        if not v:
            raise ValueError('Email is required')
        return v.lower()
    
    @validator('password')
    def validate_password(cls, v):
        if not v:
            raise ValueError('Password is required')
        return v

class ClassDifficultySubmission(BaseModel):
    class_code: str  # e.g., "COMP 550"
    class_name: str  # e.g., "Algorithms and Data Structures"
    major: str
    difficulty_rating: int
    professor: str
    semester: str  # e.g., "Fall 2024"
    user_id: str
    
    @validator('class_code')
    def validate_class_code(cls, v):
        if not v.strip():
            raise ValueError('Class code is required')
        # Basic format validation: Letters + numbers
        if not re.match(r'^[A-Z]{2,4}\s+\d{3,4}[A-Z]?$', v.strip().upper()):
            raise ValueError('Class code must be in format like "COMP 550" or "MATH 231"')
        return v.strip().upper()
    
    @validator('class_name')
    def validate_class_name(cls, v):
        if not v.strip():
            raise ValueError('Class name is required')
        if len(v) > 200:
            raise ValueError('Class name too long (max 200 characters)')
        return v.strip()
    
    @validator('difficulty_rating')
    def validate_difficulty_rating(cls, v):
        if v < 1 or v > 10:
            raise ValueError('Difficulty rating must be between 1 and 10')
        return v
    
    @validator('professor')
    def validate_professor(cls, v):
        if not v.strip():
            raise ValueError('Professor name is required')
        if len(v) > 100:
            raise ValueError('Professor name too long (max 100 characters)')
        return v.strip()
    
    @validator('semester')
    def validate_semester(cls, v):
        if not v.strip():
            raise ValueError('Semester is required')
        # Basic validation for semester format
        if not re.match(r'^(Fall|Spring|Summer)\s+\d{4}$', v.strip()):
            raise ValueError('Semester must be in format like "Fall 2024"')
        return v.strip()

class ProfessorRating(BaseModel):
    professor: str
    class_code: str
    rating: float  # 1-5 stars
    review: Optional[str] = ""
    major: str
    semester: str
    user_id: str
    
    @validator('professor')
    def validate_professor(cls, v):
        if not v.strip():
            raise ValueError('Professor name is required')
        return v.strip()
    
    @validator('rating')
    def validate_rating(cls, v):
        if v < 1.0 or v > 5.0:
            raise ValueError('Rating must be between 1.0 and 5.0')
        return round(v, 1)
    
    @validator('review')
    def validate_review(cls, v):
        if v and len(v) > 1000:
            raise ValueError('Review too long (max 1000 characters)')
        return v.strip() if v else ""

class ClassRanking(BaseModel):
    class_code: str
    class_name: str
    major: str
    average_difficulty: float
    total_submissions: int
    professors: List[dict]  # [{name: str, avg_rating: float, rating_count: int}]

class MajorStats(BaseModel):
    major: str
    total_classes: int
    total_users: int
    average_difficulty: float