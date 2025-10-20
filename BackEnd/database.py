"""Enhanced database operations for the revamped site"""
import hashlib
import bcrypt
from datetime import datetime
from typing import List, Optional, Dict, Any
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.collection import Collection
from mongo_db import mongo_db
from auth_models import (
    User, UserCreate, ClassDifficultySubmission, 
    ProfessorRating, ClassRanking, MajorStats
)

class DatabaseManager:
    def __init__(self):
        self.db = mongo_db.db
        self.users: Collection = self.db.users
        self.class_submissions: Collection = self.db.class_submissions
        self.professor_ratings: Collection = self.db.professor_ratings
        
        # Create indexes for better performance
        self._create_indexes()
    
    def _create_indexes(self):
        """Create database indexes for better query performance"""
        # Users collection indexes
        self.users.create_index("email", unique=True)
        self.users.create_index("major")
        self.users.create_index("grad_year")
        
        # Class submissions collection indexes
        self.class_submissions.create_index([("major", ASCENDING), ("class_code", ASCENDING)])
        self.class_submissions.create_index([("class_code", ASCENDING), ("major", ASCENDING)])
        self.class_submissions.create_index("user_id")
        self.class_submissions.create_index("professor")
        
        # Professor ratings collection indexes
        self.professor_ratings.create_index([("professor", ASCENDING), ("class_code", ASCENDING)])
        self.professor_ratings.create_index([("major", ASCENDING), ("professor", ASCENDING)])
        self.professor_ratings.create_index("user_id")
    
    def _hash_password(self, password: str) -> str:
        """Hash a password using bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def _verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    def create_user(self, user_data: UserCreate) -> User:
        """Create a new user with hashed password"""
        # Check if user already exists
        existing_user = self.users.find_one({"email": user_data.email})
        if existing_user:
            raise ValueError("User with this email already exists")
        
        # Hash the password
        hashed_password = self._hash_password(user_data.password)
        
        # Generate display name (e.g., "Computer Science 2028")
        display_name = f"{user_data.major} {user_data.grad_year}"
        
        user_dict = {
            "email": user_data.email,
            "password_hash": hashed_password,
            "major": user_data.major,
            "grad_year": user_data.grad_year,
            "display_name": display_name,
            "created_at": datetime.utcnow(),
            "is_active": True,
            "email_verified": False  # For future email verification
        }
        
        result = self.users.insert_one(user_dict)
        user_dict["id"] = str(result.inserted_id)
        
        # Don't return password hash in user object
        user_dict.pop("password_hash", None)
        return User(**user_dict)
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email (without password hash)"""
        user_doc = self.users.find_one({"email": email.lower()})
        if user_doc:
            user_doc["id"] = str(user_doc["_id"])
            user_doc.pop("password_hash", None)  # Don't include password hash
            return User(**user_doc)
        return None
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user with email and password"""
        user_doc = self.users.find_one({"email": email.lower()})
        if not user_doc:
            return None
        
        # Verify password
        if not self._verify_password(password, user_doc["password_hash"]):
            return None
        
        # Return user without password hash
        user_doc["id"] = str(user_doc["_id"])
        user_doc.pop("password_hash", None)
        return User(**user_doc)
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        from bson import ObjectId
        try:
            user_doc = self.users.find_one({"_id": ObjectId(user_id)})
            if user_doc:
                user_doc["id"] = str(user_doc["_id"])
                return User(**user_doc)
        except:
            pass
        return None
    
    def submit_class_difficulty(self, submission: ClassDifficultySubmission) -> bool:
        """Submit a class difficulty rating"""
        submission_dict = submission.dict()
        submission_dict["submitted_at"] = datetime.utcnow()
        
        # Debug logging
        print(f"DEBUG: Submitting difficulty for user_id: {submission.user_id}, class: {submission.class_code}, major: {submission.major}")
        
        # Check if user already submitted for this class
        existing = self.class_submissions.find_one({
            "user_id": submission.user_id,
            "class_code": submission.class_code,
            "major": submission.major
        })
        
        if existing:
            # Update existing submission
            print(f"DEBUG: Updating existing submission {existing['_id']}")
            self.class_submissions.update_one(
                {"_id": existing["_id"]},
                {"$set": submission_dict}
            )
        else:
            # Create new submission
            print(f"DEBUG: Creating new submission")
            result = self.class_submissions.insert_one(submission_dict)
            print(f"DEBUG: Inserted with ID: {result.inserted_id}")
        
        return True
    
    def submit_professor_rating(self, rating: ProfessorRating) -> bool:
        """Submit a professor rating"""
        rating_dict = rating.dict()
        rating_dict["submitted_at"] = datetime.utcnow()
        
        # Check if user already rated this professor for this class
        existing = self.professor_ratings.find_one({
            "user_id": rating.user_id,
            "professor": rating.professor,
            "class_code": rating.class_code
        })
        
        if existing:
            # Update existing rating
            self.professor_ratings.update_one(
                {"_id": existing["_id"]},
                {"$set": rating_dict}
            )
        else:
            # Create new rating
            self.professor_ratings.insert_one(rating_dict)
        
        return True
    
    def get_class_rankings_by_major(self, major: str, limit: int = 50) -> List[ClassRanking]:
        """Get class rankings for a specific major, sorted by difficulty"""
        pipeline = [
            {"$match": {"major": major}},
            {
                "$group": {
                    "_id": {
                        "class_code": "$class_code",
                        "class_name": "$class_name",
                        "major": "$major"
                    },
                    "average_difficulty": {"$avg": "$difficulty_rating"},
                    "total_submissions": {"$sum": 1},
                    "professors": {"$addToSet": "$professor"}
                }
            },
            {"$sort": {"average_difficulty": DESCENDING}},
            {"$limit": limit}
        ]
        
        results = list(self.class_submissions.aggregate(pipeline))
        rankings = []
        
        for result in results:
            # Get professor ratings for this class
            professor_stats = []
            for prof in result["professors"]:
                prof_ratings = list(self.professor_ratings.find({
                    "professor": prof,
                    "class_code": result["_id"]["class_code"],
                    "major": major
                }))
                
                if prof_ratings:
                    avg_rating = sum(r["rating"] for r in prof_ratings) / len(prof_ratings)
                    professor_stats.append({
                        "name": prof,
                        "avg_rating": round(avg_rating, 1),
                        "rating_count": len(prof_ratings)
                    })
                else:
                    professor_stats.append({
                        "name": prof,
                        "avg_rating": 0.0,
                        "rating_count": 0
                    })
            
            # Sort professors by rating
            professor_stats.sort(key=lambda x: x["avg_rating"], reverse=True)
            
            ranking = ClassRanking(
                class_code=result["_id"]["class_code"],
                class_name=result["_id"]["class_name"],
                major=result["_id"]["major"],
                average_difficulty=round(result["average_difficulty"], 1),
                total_submissions=result["total_submissions"],
                professors=professor_stats
            )
            rankings.append(ranking)
        
        return rankings
    
    def get_all_majors(self) -> List[str]:
        """Get all unique majors that have submissions"""
        majors = self.class_submissions.distinct("major")
        return sorted(majors)
    
    def get_major_stats(self, major: str) -> MajorStats:
        """Get statistics for a specific major"""
        # Count unique classes
        unique_classes = len(self.class_submissions.distinct("class_code", {"major": major}))
        
        # Count users in this major
        user_count = self.users.count_documents({"major": major})
        
        # Get average difficulty across all classes
        pipeline = [
            {"$match": {"major": major}},
            {
                "$group": {
                    "_id": None,
                    "avg_difficulty": {"$avg": "$difficulty_rating"}
                }
            }
        ]
        
        avg_result = list(self.class_submissions.aggregate(pipeline))
        avg_difficulty = avg_result[0]["avg_difficulty"] if avg_result else 0.0
        
        return MajorStats(
            major=major,
            total_classes=unique_classes,
            total_users=user_count,
            average_difficulty=round(avg_difficulty, 1)
        )
    
    def get_professor_ratings(self, professor: str, class_code: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get ratings for a specific professor, optionally filtered by class"""
        query = {"professor": professor}
        if class_code:
            query["class_code"] = class_code
        
        ratings = list(self.professor_ratings.find(query))
        for rating in ratings:
            rating["id"] = str(rating.pop("_id"))
        
        return ratings
    
    def get_database_health(self):
        """Check database health for monitoring"""
        try:
            # Test database connection
            self.db.command('ping')
            
            # Get database stats
            stats = self.db.command("dbStats")
            
            return {
                "status": "healthy",
                "database": self.db.name,
                "collections": stats.get("collections", 0),
                "dataSize": stats.get("dataSize", 0),
                "storageSize": stats.get("storageSize", 0)
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "database": self.db.name if self.db else "unknown"
            }

# Global database manager instance
db_manager = DatabaseManager()