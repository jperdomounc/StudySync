"""
Revamped StudySync API - UNC Class and Professor Rating System
"""
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Optional
import jwt
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
from auth_models import (
    User, UserCreate, LoginRequest, ClassDifficultySubmission, 
    ProfessorRating, ClassRanking, MajorStats
)
from database import db_manager

app = FastAPI(title="StudySync - UNC Class Rating System", version="2.0.0")

# Security
security = HTTPBearer()
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "fallback-secret-key-for-dev")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# CORS Configuration
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def create_access_token(user_id: str, expires_delta: Optional[timedelta] = None):
    """Create JWT access token"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=7)  # 7 days expiry
    
    to_encode = {"user_id": user_id, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token and return user ID"""
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
        return user_id
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

def get_current_user(user_id: str = Depends(verify_token)) -> User:
    """Get current authenticated user"""
    user = db_manager.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

# Health check
@app.get("/")
async def root():
    return {
        "message": "StudySync API v2.0 - UNC Class Rating System",
        "status": "active",
        "timestamp": datetime.utcnow()
    }

# Authentication endpoints
@app.post("/auth/register", response_model=dict)
def register_user(user_data: UserCreate):
    """Register a new user with UNC email"""
    try:
        user = db_manager.create_user(user_data)
        access_token = create_access_token(user.id)
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "display_name": user.display_name,
                "major": user.major,
                "grad_year": user.grad_year
            }
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Registration failed")

@app.post("/auth/login", response_model=dict)
def login_user(login_data: LoginRequest):
    """Login user with email and password"""
    user = db_manager.authenticate_user(login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is deactivated"
        )
    
    access_token = create_access_token(user.id)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "display_name": user.display_name,
            "major": user.major,
            "grad_year": user.grad_year
        }
    }

@app.get("/auth/me", response_model=User)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Get current user profile"""
    return current_user

# Major endpoints
@app.get("/majors", response_model=List[str])
def get_all_majors():
    """Get all available majors"""
    try:
        majors = db_manager.get_all_majors()
        return majors
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve majors")

@app.get("/majors/{major}/stats", response_model=MajorStats)
def get_major_statistics(major: str):
    """Get statistics for a specific major"""
    try:
        stats = db_manager.get_major_stats(major)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve major statistics")

@app.get("/majors/{major}/classes", response_model=List[ClassRanking])
def get_class_rankings(major: str, limit: int = 50):
    """Get class difficulty rankings for a specific major"""
    try:
        rankings = db_manager.get_class_rankings_by_major(major, limit)
        return rankings
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve class rankings")

# Class difficulty submission endpoints
@app.post("/submissions/difficulty")
def submit_class_difficulty(
    submission: ClassDifficultySubmission,
    current_user: User = Depends(get_current_user)
):
    """Submit a class difficulty rating"""
    try:
        # Set the user_id from the authenticated user
        submission.user_id = current_user.id
        
        # Ensure the submission is for the user's major
        if submission.major != current_user.major:
            raise HTTPException(
                status_code=400,
                detail="You can only submit ratings for your own major"
            )
        
        success = db_manager.submit_class_difficulty(submission)
        if success:
            return {"message": "Difficulty rating submitted successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to submit rating")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to submit rating")

# Professor rating endpoints
@app.post("/submissions/professor")
def submit_professor_rating(
    rating: ProfessorRating,
    current_user: User = Depends(get_current_user)
):
    """Submit a professor rating"""
    try:
        # Set the user_id from the authenticated user
        rating.user_id = current_user.id
        
        # Ensure the rating is for the user's major
        if rating.major != current_user.major:
            raise HTTPException(
                status_code=400,
                detail="You can only submit ratings for your own major"
            )
        
        success = db_manager.submit_professor_rating(rating)
        if success:
            return {"message": "Professor rating submitted successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to submit rating")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to submit rating")

@app.get("/professors/{professor}/ratings")
def get_professor_ratings(professor: str, class_code: Optional[str] = None):
    """Get ratings for a specific professor"""
    try:
        ratings = db_manager.get_professor_ratings(professor, class_code)
        return {
            "professor": professor,
            "class_code": class_code,
            "ratings": ratings
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve professor ratings")

# Admin endpoints (for future use)
@app.get("/admin/users", response_model=List[dict])
def get_all_users(current_user: User = Depends(get_current_user)):
    """Get all users (admin only)"""
    # In a real application, you'd check if the user is an admin
    # For now, we'll just return basic info
    try:
        # This is a placeholder - implement proper admin checks
        return {"message": "Admin functionality not implemented yet"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve users")

# Health check endpoints
@app.get("/health")
async def health_check():
    """Comprehensive health check endpoint"""
    try:
        # Check database connection
        db_health = db_manager.get_database_health()
        
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow(),
            "version": "2.0.0",
            "environment": ENVIRONMENT,
            "database": db_health,
            "services": {
                "auth": "operational",
                "ratings": "operational"
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.utcnow()
            }
        )

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)