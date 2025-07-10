import json
import random

def generate_mock_professor_ratings():
    """Generate mock professor ratings for testing purposes since RMP API has changed"""
    
    # Load existing professors from professors.json
    with open("professors.json", "r") as f:
        professors = json.load(f)
    
    # Add mock ratings to professors
    for prof in professors:
        # Generate realistic ratings
        prof["rating"] = round(random.uniform(2.5, 4.8), 1)
        prof["difficulty"] = round(random.uniform(1.2, 4.5), 1)
        prof["numRatings"] = random.randint(5, 150)
        prof["wouldTakeAgain"] = random.choice([True, False])
    
    # Save updated professors with ratings
    with open("professors_with_ratings.json", "w") as f:
        json.dump(professors, f, indent=2)
    
    print(f"✅ Generated mock ratings for {len(professors)} professors")
    print("📝 Note: Using mock data since RateMyProfessor API has changed")
    return professors

def load_professor_ratings():
    """Load professor ratings from file"""
    try:
        with open("professors_with_ratings.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return generate_mock_professor_ratings()

if __name__ == "__main__":
    generate_mock_professor_ratings()
