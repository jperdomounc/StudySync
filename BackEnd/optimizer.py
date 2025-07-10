"""optimize schedule algorithm"""
import json
from typing import List, Dict
from models import Course

class ScheduleOptimizer:
    def __init__(self):
        self.professor_ratings = self.load_professor_ratings()
        
    def load_professor_ratings(self) -> Dict[str, Dict]:
        """Load professor ratings from file"""
        try:
            with open("professors_with_ratings.json", "r") as f:
                professors = json.load(f)
                # Create a lookup dict by professor name
                return {prof["name"]: prof for prof in professors}
        except FileNotFoundError:
            return {}
    
    def get_professor_rating(self, instructor_name: str) -> float:
        """Get professor rating, return default if not found"""
        if instructor_name in self.professor_ratings:
            return self.professor_ratings[instructor_name].get("rating", 3.0)
        return 3.0  # Default rating
    
    def check_time_conflict(self, course1: Course, course2: Course) -> bool:
        """Check if two courses have time conflicts"""
        # Check if they share any days
        shared_days = set(course1.days) & set(course2.days)
        if not shared_days:
            return False
        
        # Convert time strings to minutes for comparison
        def time_to_minutes(time_str):
            hours, minutes = map(int, time_str.split(':'))
            return hours * 60 + minutes
        
        start1 = time_to_minutes(course1.start_time)
        end1 = time_to_minutes(course1.end_time)
        start2 = time_to_minutes(course2.start_time)
        end2 = time_to_minutes(course2.end_time)
        
        # Check for overlap
        return not (end1 <= start2 or end2 <= start1)
    
    def generate_all_schedules(self, courses: List[Course]) -> List[List[Course]]:
        """Generate all possible non-conflicting schedules"""
        valid_schedules = []
        
        # Group courses by subject/number to handle sections
        course_groups = {}
        for course in courses:
            # Extract course code (e.g., "BIOL 101" from "BIOL 101 001")
            parts = course.title.split()
            if len(parts) >= 2:
                course_key = f"{parts[0]} {parts[1]}"
                if course_key not in course_groups:
                    course_groups[course_key] = []
                course_groups[course_key].append(course)
        
        # Generate combinations of one section per course
        def generate_combinations(groups, current_combo=[]):
            if not groups:
                # Check if current combination has no conflicts
                if self.is_valid_schedule(current_combo):
                    valid_schedules.append(current_combo[:])
                return
            
            group = groups[0]
            remaining = groups[1:]
            
            for course in group:
                # Check if this course conflicts with current combo
                conflicts = any(self.check_time_conflict(course, existing) 
                              for existing in current_combo)
                if not conflicts:
                    current_combo.append(course)
                    generate_combinations(remaining, current_combo)
                    current_combo.pop()
        
        generate_combinations(list(course_groups.values()))
        return valid_schedules
    
    def is_valid_schedule(self, schedule: List[Course]) -> bool:
        """Check if schedule has no time conflicts"""
        for i in range(len(schedule)):
            for j in range(i + 1, len(schedule)):
                if self.check_time_conflict(schedule[i], schedule[j]):
                    return False
        return True
    
    def score_schedule(self, schedule: List[Course]) -> float:
        """Score a schedule based on professor ratings and other factors"""
        if not schedule:
            return 0.0
        
        # Base score from professor ratings
        rating_score = sum(self.get_professor_rating(course.instructor) 
                          for course in schedule) / len(schedule)
        
        # Bonus for fewer early morning classes (before 9 AM)
        early_penalty = sum(1 for course in schedule 
                           if course.start_time < "09:00") * 0.1
        
        # Bonus for fewer late classes (after 6 PM)
        late_penalty = sum(1 for course in schedule 
                          if course.start_time >= "18:00") * 0.1
        
        # Bonus for having gaps between classes (not too packed)
        gap_bonus = self.calculate_gap_bonus(schedule)
        
        return rating_score - early_penalty - late_penalty + gap_bonus
    
    def calculate_gap_bonus(self, schedule: List[Course]) -> float:
        """Calculate bonus for having reasonable gaps between classes"""
        # This is a simplified implementation
        # In practice, you'd want to analyze the daily schedule
        return 0.1  # Small bonus for now
    
    def optimize_schedule(self, courses: List[Course], max_schedules: int = 10) -> List[List[Course]]:
        """Find the best schedules based on professor ratings"""
        all_schedules = self.generate_all_schedules(courses)
        
        if not all_schedules:
            return []
        
        # Score and sort schedules
        scored_schedules = [(self.score_schedule(schedule), schedule) 
                           for schedule in all_schedules]
        scored_schedules.sort(key=lambda x: x[0], reverse=True)
        
        # Return top schedules
        return [schedule for _, schedule in scored_schedules[:max_schedules]]
    
    def find_schedule_with_additional_course(self, 
                                           existing_schedule: List[Course], 
                                           new_course_title: str,
                                           available_courses: List[Course]) -> List[Course]:
        """Find a schedule that fits an additional course"""
        # Find sections of the requested course
        matching_courses = [c for c in available_courses 
                           if new_course_title.lower() in c.title.lower()]
        
        if not matching_courses:
            return existing_schedule
        
        # Try to fit each section with the existing schedule
        for course in matching_courses:
            # Check if this course conflicts with existing schedule
            conflicts = any(self.check_time_conflict(course, existing) 
                          for existing in existing_schedule)
            
            if not conflicts:
                # Found a compatible section
                new_schedule = existing_schedule + [course]
                return new_schedule
        
        # If no section fits, try to find alternative schedule
        all_courses = existing_schedule + matching_courses
        optimized = self.optimize_schedule(all_courses, max_schedules=1)
        
        if optimized:
            return optimized[0]
        
        return existing_schedule