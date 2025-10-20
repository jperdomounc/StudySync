#!/usr/bin/env python3
"""
StudySync Database Initialization Script
Populates the database with UNC course data for testing and demonstration
"""

import random
from datetime import datetime, timedelta
from mongo_db import mongo_db
from database import db_manager
from auth_models import ClassDifficultySubmission, ProfessorRating
import hashlib

# Sample professor names for realistic data
SAMPLE_PROFESSORS = [
    "Dr. Smith", "Prof. Johnson", "Dr. Williams", "Prof. Brown", "Dr. Jones",
    "Prof. Garcia", "Dr. Miller", "Prof. Davis", "Dr. Rodriguez", "Prof. Martinez",
    "Dr. Anderson", "Prof. Taylor", "Dr. Thomas", "Prof. Jackson", "Dr. White",
    "Prof. Harris", "Dr. Martin", "Prof. Thompson", "Dr. Garcia", "Prof. Lee",
    "Dr. Walker", "Prof. Hall", "Dr. Allen", "Prof. Young", "Dr. King",
    "Prof. Wright", "Dr. Lopez", "Prof. Hill", "Dr. Scott", "Prof. Green",
    "Dr. Adams", "Prof. Baker", "Dr. Gonzalez", "Prof. Nelson", "Dr. Carter",
    "Prof. Mitchell", "Dr. Perez", "Prof. Roberts", "Dr. Turner", "Prof. Phillips"
]

# UNC Course Data by Major
UNC_COURSES = {
    "Art": [
        "ARTS 102 – Two-Dimensional Design",
        "ARTS 104 – Drawing I",
        "ARTS 105 – Photography I",
        "ARTS 115 – Darkroom Photography I",
        "ARTS 132 – Collage: Strategies for Thinking and Making",
        "ARTS 202 – Painting I",
        "ARTS 208 – Print I",
        "ARTS 103 – Sculpture I",
        "ARTS 213 – Ceramic I",
        "ARTS 233 – Wood Sculpture",
        "ARTS 106 – Video I",
        "ARTS 116 – Introduction to Web Media",
        "ARTS 205 – Photography II",
        "ARTS 206 – Video II",
        "ARTS 209 – 2D Animation",
        "ARTS 214 – Life Drawing",
        "ARTS 215 – Darkroom Photography II",
        "ARTS 221 – Color: Theory and Concept",
        "ARTS 222 – New Technologies and Narrative Painting",
        "ARTS 238 – Screen Printing",
        "ARTS 290 – Special Topics in Studio Art",
        "ARTS 302 – Painting II",
        "ARTS 313 – Ceramic II",
        "ARTS 324 – Drawing II",
        "ARTS 352 – Abstract Painting",
        "ARTS 358 – Letterpress",
        "ARTS 368 – Print II",
        "ARTS 309 – 3D Animation",
        "ARTS 322 – Narrative Painting",
        "ARTS 343 – MAKE: Art in the (New) Age",
        "ARTS 353 – Phantasmagoria: Haunted Art, History, and Installation",
        "ARTS 354 – Narrative Drawing",
        "ARTS 355 – The Practice of Representation: Portraiture in Photography",
        "ARTS 363 – At the Radical Edge of Life: Art, Space, and Ecology",
        "ARTS 364 – The Walking Seminar: A Territorial Investigation",
        "ARTS 383 – States of Change",
        "ARTS 390 – Special Topics in Studio Art",
        "ARTS 402 – Advanced Painting Projects",
        "ARTS 409 – Art and Science: Merging Printmaking and Biology",
        "ARTS 410 – Public Art",
        "ARTS 413 – Advanced Ceramic Projects",
        "ARTS 415 – Conceptual-Experimental Photography",
        "ARTS 416 – Advanced Video",
        "ARTS 417 – Advanced Mixed Media Projects",
        "ARTS 418 – Advanced Printmaking",
        "ARTS 428 – Book Art",
        "ARTS 458 – Photo Printmaking",
        "ARTS 490 – Advanced Special Topics in Studio Art",
        "ARTS 493 – Studio Art Practicum or Internship",
        "ARTS 515 – Advanced Topics in Photography",
        "ARTS 596 – Independent Study in Studio Art"
    ],
    
    "Applied Sciences": [
        "APPL 101 – Exploring Engineering",
        "APPL 110 – Design and Making for Engineers: Developing Your Personal Design Potential",
        "COMP 110 – Introduction to Programming",
        "COMP 116 – Introduction to Scientific Programming",
        "APPL 240 – Electronics from Sensors to Indicators: Circuits that Interact with the Physical World",
        "APPL 260 – Materials Science and Engineering: Living in a Material World",
        "APPL 285 – Engineering Fundamentals of Force, Motion, and Energy",
        "APPL 385 – Thermodynamics for Engineers",
        "APPL 697 – Capstone Design I",
        "APPL 698 – Capstone Design II",
        "CHEM 101 – General Descriptive Chemistry I",
        "CHEM 101L – Quantitative Chemistry Laboratory I",
        "CHEM 102 – General Descriptive Chemistry II",
        "CHEM 102L – Quantitative Chemistry Laboratory II",
        "MATH 231 – Calculus of Functions of One Variable I",
        "MATH 232 – Calculus of Functions of One Variable II",
        "MATH 233 – Calculus of Functions of Several Variables",
        "MATH 383 – First Course in Differential Equations",
        "MATH 383L – Laboratory",
        "PHYS 118 – Introductory Calculus-based Mechanics and Relativity",
        "PHYS 119 – Introductory Calculus-based Electromagnetism and Quanta",
        "ENVR 205 – Engineering Tools for Environmental Problem Solving",
        "ENVR 205L – Lab",
        "ENVR 419 – Chemical Equilibria in Natural Waters",
        "ENVR 421 – Environmental Health Microbiology",
        "ENVR 548 – Sustainable Energy Systems",
        "ENVR 675 – Air Pollution, Chemistry, and Physics",
        "ENVR 451 – Introduction to Environmental Modeling",
        "ENVR 453 – Groundwater Hydrology",
        "ENVR 468 – Temporal GIS and Space/Time Geostatistics for the Environment and Public Health",
        "ENVR 635 – Energy Modeling for Environment and Public Health",
        "ENVR 730 – Computational Toxicology and Exposure Science",
        "ENVR 656 – Physical/Chemical Processes for Water Treatment",
        "ENVR 710 – Environmental Process Biotechnology",
        "ENVR 755 – Analysis of Water Resource Systems",
        "APPL 462 – Engineering Materials: Properties, Selection and Design",
        "APPL 430 – Optoelectronics from Materials to Devices",
        "APPL 435 – Nanophotonics",
        "APPL 463 – Bioelectronic Materials",
        "APPL 465 – Engineering of Soft Materials: SpongeBob Squarepants and Other Squishy Things",
        "APPL 467 – Materials Design for Biomedicine"
    ],
    
    "Biology": [
        "BIOL 101 – Principles of Biology",
        "BIOL 101L – Introductory Biology Laboratory",
        "BIOL 103 – How Cells Function",
        "BIOL 104 – Biodiversity",
        "BIOL 105L – Biological Research Skills",
        "BIOL 220 – Molecular Genetics",
        "BIOL 240 – Cell Biology",
        "BIOL 250 – Evolutionary Biology",
        "BIOL 260 – Introduction to Ecology",
        "BIOL 271 – Plant Biology",
        "BIOL 271L – Plant Biology Laboratory",
        "BIOL 272 – Local Flora",
        "BIOL 272L – Local Flora Lab",
        "BIOL 273 – Horticulture",
        "BIOL 274 – Plant Diversity",
        "BIOL 274L – Plant Diversity Laboratory",
        "BIOL 277 – Vertebrate Field Zoology",
        "BIOL 277L – Vertebrate Field Zoology Laboratory",
        "BIOL 278 – Animal Behavior",
        "BIOL 278L – Animal Behavior Laboratory",
        "BIOL 279 – Seminar in Organismal Biology",
        "BIOL 279L – Topics in Organismal Biology Laboratory",
        "BIOL 422 – Microbiology",
        "BIOL 421L – Bacterial Genetics Laboratory",
        "BIOL 422L – Microbiology Laboratory",
        "BIOL 441 – Vertebrate Embryology",
        "BIOL 441L – Vertebrate Embryology Laboratory",
        "BIOL 451 – Comparative Physiology",
        "BIOL 451L – Comparative Physiology Laboratory",
        "BIOL 471 – Evolutionary Mechanisms",
        "BIOL 471L – Evolutionary Mechanisms Laboratory",
        "BIOL 473 – Mammalian Morphology and Development",
        "BIOL 473L – Mammalian Morphology Laboratory",
        "BIOL 474 – Evolution of Vertebrate Life",
        "BIOL 474L – Vertebrate Structure and Evolution Laboratory",
        "BIOL 475 – Biology of Marine Animals",
        "BIOL 475L – Biology of Marine Animals Laboratory",
        "BIOL 476 – Avian Biology",
        "BIOL 476L – Avian Biology Laboratory",
        "BIOL 479 – Topics in Organismal Biology at an Advanced Level",
        "BIOL 479L – Laboratory in Organismal Biology: Advanced Topics",
        "BIOL 579 – Organismal Structure and Diversity in the Southern Appalachian Mountains"
    ],

    "Computer Science": [
        "COMP 210 – Data Structures and Analysis",
        "COMP 211 – Systems Fundamentals",
        "COMP 301 – Foundations of Programming",
        "COMP 311 – Computer Organization",
        "COMP 283 – Discrete Structures",
        "COMP 455 – Models of Languages and Computation",
        "COMP 550 – Algorithms and Analysis",
        "COMP 426 – Modern Web Programming",
        "COMP 431 – Internet Services and Protocols",
        "COMP 435 – Computer Security Concepts",
        "COMP 440 – Database Systems",
        "COMP 445 – Algorithms and Data Structures",
        "COMP 460 – Algorithms for Computational Biology",
        "COMP 475 – 2D Computer Graphics",
        "COMP 476 – 3D Computer Graphics",
        "COMP 480 – Analog and Digital Communication",
        "COMP 486 – Applications of Natural Language Processing",
        "COMP 487 – Information Retrieval",
        "COMP 520 – Compilers",
        "COMP 521 – Files and Databases",
        "COMP 522 – Modeling and Design of Computer Systems",
        "COMP 523 – Software Engineering Laboratory",
        "COMP 524 – Programming Language Concepts",
        "COMP 530 – Operating Systems",
        "COMP 533 – Distributed Systems",
        "COMP 535 – Computer Security",
        "COMP 541 – Digital Logic and Computer Design",
        "COMP 542 – Machine Learning",
        "COMP 545 – Computational Geometry",
        "COMP 550 – Algorithms and Analysis",
        "COMP 555 – Bioalgorithms",
        "COMP 560 – Artificial Intelligence",
        "COMP 562 – Introduction to Machine Learning",
        "COMP 565 – Introduction to Data Science",
        "COMP 570 – Artificial Intelligence",
        "COMP 575 – Introduction to Computer Graphics",
        "COMP 580 – Enabling Technologies",
        "COMP 585 – Serious Games",
        "COMP 590 – Topics in Computer Science"
    ],

    "Data Science": [
        "DATA 110 – Introduction to Data Science",
        "DATA 120 – Ethics of AI and Societal Decision Making",
        "DATA 150 – Communication for Data Scientists",
        "DATA 521 – Foundations in Artificial Intelligence",
        "COMP 301 – Foundations of Programming",
        "COMP 562 – Introduction to Machine Learning",
        "BIOS 511 – Introduction to Statistical Computing and Data Management",
        "BIOS 512 – Data Science Basics",
        "BIOS 635 – Introduction to Machine Learning",
        "BIOS 650 – Basic Elements of Probability and Statistical Inference I",
        "STOR 120 – Foundations of Statistics and Data Science",
        "STOR 320 – Methods and Models of Data Science",
        "STOR 415 – Introduction to Optimization",
        "STOR 435 – Introduction to Probability",
        "STOR 520 – Statistical Computing for Data Science",
        "STOR 535 – Probability for Data Science",
        "STOR 565 – Machine Learning",
        "STOR 566 – Introduction to Deep Learning",
        "STOR 572 – Simulation for Analytics",
        "STOR 612 – Foundations of Optimization",
        "STOR 634 – Probability I",
        "MATH 347 – Linear Algebra for Applications",
        "MATH 381 – Discrete Mathematics",
        "MATH 521 – Advanced Calculus I",
        "MATH 522 – Advanced Calculus II",
        "MATH 524 – Elementary Differential Equations",
        "MATH 560 – Optimization with Applications in Machine Learning",
        "MATH 566 – Introduction to Numerical Analysis",
        "MATH 577 – Linear Algebra",
        "MATH 661 – Scientific Computation I"
    ],

    "Economics": [
        "ECON 101 – Introduction to Economics",
        "ECON 400 – Introduction to Data Science and Econometrics",
        "ECON 410 – Intermediate Microeconomics",
        "ECON 420 – Intermediate Macroeconomics",
        "ECON 470 – Econometrics",
        "ECON 425 – Economics of Developing Countries",
        "ECON 430 – Money and Banking",
        "ECON 435 – Labor Economics",
        "ECON 445 – Industrial Organization",
        "ECON 450 – Public Economics",
        "ECON 460 – International Economics",
        "ECON 465 – Environmental Economics",
        "ECON 480 – Game Theory",
        "ECON 485 – Economics of Information",
        "ECON 490 – Topics in Economics",
        "ECON 520 – Advanced Microeconomics",
        "ECON 525 – Advanced Macroeconomics",
        "ECON 530 – Mathematical Economics",
        "ECON 535 – Econometric Methods",
        "ECON 540 – Advanced Topics in Econometrics",
        "ECON 545 – Health Economics",
        "ECON 550 – Advanced Health Econometrics",
        "ECON 552 – The Economics of Health Care Markets and Policy",
        "ECON 555 – Behavioral Economics",
        "ECON 560 – Financial Economics",
        "ECON 565 – Urban Economics",
        "ECON 570 – Economic History",
        "ECON 575 – Economics of Education",
        "ECON 580 – Experimental Economics"
    ],

    "Business Administration": [
        "BUSI 401 – Management and Corporate Communication",
        "BUSI 402 – Applied Microeconomics for Business",
        "BUSI 403 – Operations Management",
        "BUSI 404 – Business Ethics",
        "BUSI 405 – Leading and Managing: An Introduction to Organizational Behavior",
        "BUSI 406 – Marketing",
        "BUSI 407 – Financial Accounting",
        "BUSI 408 – Corporate Finance",
        "BUSI 410 – Business Analytics",
        "BUSI 411 – Strategy I: Competitive Strategy",
        "BUSI 412 – Strategy II: Global Corporate Strategy",
        "BUSI 500 – Entrepreneurship and Business Planning",
        "BUSI 501 – Professional Selling Strategies and Skills",
        "BUSI 502 – Entrepreneurial Finance",
        "BUSI 505 – Entrepreneurial Consulting",
        "BUSI 506 – Venture Capital Fundamentals",
        "BUSI 507 – Sustainable Business and Social Enterprise",
        "BUSI 508 – Sustainable Business and Impact Entrepreneurship",
        "BUSI 520 – Advanced Spreadsheet Modeling for Business",
        "BUSI 523 – Diversity and Inclusion at Work",
        "BUSI 525 – Advanced Business Presentations",
        "BUSI 530 – Corporate Communication: Social Advocacy and Activism",
        "BUSI 533 – Supply Chain Management",
        "BUSI 540 – Leadership for Wicked Problems",
        "BUSI 545 – Negotiations",
        "BUSI 547 – Managerial Decision Making",
        "BUSI 550 – People Analytics",
        "BUSI 555 – Groups and Teams in Organizations",
        "BUSI 558 – Digital Marketing",
        "BUSI 559 – Product Management",
        "BUSI 562 – Consumer Behavior",
        "BUSI 563 – Retail & E-tail Marketing",
        "BUSI 564 – Design Thinking and Product Development",
        "BUSI 566 – Marketing Strategy: Sustainable Competitive Advantage in Dynamic Environments",
        "BUSI 568 – Customer Insights and Analytics",
        "BUSI 574 – Taxes and Business Strategy",
        "BUSI 575 – Financial Statement Analysis and Valuation",
        "BUSI 580 – Investments",
        "BUSI 582 – Mergers and Acquisitions",
        "BUSI 585 – Introduction to Real Estate",
        "BUSI 590 – Business Seminar"
    ],

    "Neuroscience": [
        "NSCI 175 – Introduction to Neuroscience",
        "NSCI 221 – Neuropsychopharmacology",
        "NSCI 222 – Learning",
        "NSCI 225 – Sensation and Perception",
        "NSCI 271 – Cellular Mechanisms in Addiction Lab",
        "NSCI 273 – Brainwaves: Human Electroencephalography Lab",
        "NSCI 274 – Neurophysiology Data Science Lab",
        "NSCI 277 – Addiction Neuroscience qPCR Laboratory",
        "NSCI 278 – Molecular Brain Imaging Lab",
        "NSCI 279 – Microglia Laboratory",
        "PSYC 101 – General Psychology",
        "PSYC 210 – Statistical Principles of Psychological Research",
        "PSYC 220 – Biopsychology",
        "PSYC 230 – Cognitive Psychology",
        "PSYC 270 – Research Methods in Psychology"
    ]
}

def parse_course_code_and_name(course_string):
    """Parse a course string like 'COMP 550 – Algorithms and Analysis' into code and name"""
    if " – " in course_string:
        code, name = course_string.split(" – ", 1)
        return code.strip(), name.strip()
    elif " - " in course_string:
        code, name = course_string.split(" - ", 1)
        return code.strip(), name.strip()
    else:
        # If no separator, treat the whole thing as the code
        return course_string.strip(), course_string.strip()

def generate_sample_user_id():
    """Generate a fake user ID for sample data"""
    return hashlib.md5(f"sample_user_{random.randint(1, 1000)}".encode()).hexdigest()[:24]

def create_sample_class_submissions(major, courses, num_submissions_per_class=3):
    """Create sample class difficulty submissions"""
    submissions = []
    
    for course_string in courses:
        code, name = parse_course_code_and_name(course_string)
        
        # Create multiple submissions per class to simulate real usage
        for _ in range(random.randint(1, num_submissions_per_class)):
            professor = random.choice(SAMPLE_PROFESSORS)
            difficulty = random.randint(3, 9)  # Most classes fall between 3-9 difficulty
            
            # Add some randomness to semesters
            current_year = datetime.now().year
            semester_options = [
                f"Fall {current_year - 1}",
                f"Spring {current_year}",
                f"Fall {current_year}",
                f"Spring {current_year + 1}"
            ]
            semester = random.choice(semester_options)
            
            submission = {
                "class_code": code,
                "class_name": name,
                "major": major,
                "difficulty_rating": difficulty,
                "professor": professor,
                "semester": semester,
                "user_id": generate_sample_user_id(),
                "submitted_at": datetime.utcnow() - timedelta(days=random.randint(1, 365))
            }
            submissions.append(submission)
    
    return submissions

def create_sample_professor_ratings(major, courses, num_ratings_per_class=2):
    """Create sample professor ratings"""
    ratings = []
    
    for course_string in courses:
        code, name = parse_course_code_and_name(course_string)
        
        # Create ratings for different professors teaching the same class
        professors_for_class = random.sample(SAMPLE_PROFESSORS, min(3, len(SAMPLE_PROFESSORS)))
        
        for professor in professors_for_class:
            for _ in range(random.randint(1, num_ratings_per_class)):
                # Professor ratings tend to be normally distributed around 3.5
                rating = round(random.gauss(3.5, 0.8), 1)
                rating = max(1.0, min(5.0, rating))  # Clamp between 1.0 and 5.0
                
                # Generate realistic reviews
                review_templates = [
                    f"Great professor! {professor} really knows the material and explains it well.",
                    f"Challenging class but {professor} is very helpful during office hours.",
                    f"I learned a lot in this class. {professor} is passionate about the subject.",
                    f"Fair grader and clear expectations. Would recommend {professor}.",
                    f"Tough but fair. {professor} really pushes students to excel.",
                    f"Engaging lectures and interesting assignments from {professor}.",
                    f"Very knowledgeable professor. {professor} made the material accessible.",
                    ""  # Some ratings have no review
                ]
                
                review = random.choice(review_templates)
                
                current_year = datetime.now().year
                semester_options = [
                    f"Fall {current_year - 1}",
                    f"Spring {current_year}",
                    f"Fall {current_year}"
                ]
                semester = random.choice(semester_options)
                
                rating_obj = {
                    "professor": professor,
                    "class_code": code,
                    "rating": rating,
                    "review": review,
                    "major": major,
                    "semester": semester,
                    "user_id": generate_sample_user_id(),
                    "submitted_at": datetime.utcnow() - timedelta(days=random.randint(1, 365))
                }
                ratings.append(rating_obj)
    
    return ratings

def initialize_database():
    """Initialize the database with sample UNC course data"""
    print("🚀 Starting StudySync database initialization...")
    
    try:
        # Clear existing data
        print("🧹 Clearing existing data...")
        db_manager.class_submissions.delete_many({})
        db_manager.professor_ratings.delete_many({})
        
        total_submissions = 0
        total_ratings = 0
        
        # Process each major
        for major, courses in UNC_COURSES.items():
            print(f"\n📚 Processing {major} major ({len(courses)} courses)...")
            
            # Create class difficulty submissions
            submissions = create_sample_class_submissions(major, courses)
            if submissions:
                db_manager.class_submissions.insert_many(submissions)
                total_submissions += len(submissions)
                print(f"   ✅ Added {len(submissions)} class difficulty submissions")
            
            # Create professor ratings
            ratings = create_sample_professor_ratings(major, courses)
            if ratings:
                db_manager.professor_ratings.insert_many(ratings)
                total_ratings += len(ratings)
                print(f"   ✅ Added {len(ratings)} professor ratings")
        
        print(f"\n🎉 Database initialization complete!")
        print(f"📊 Summary:")
        print(f"   - {len(UNC_COURSES)} majors")
        print(f"   - {sum(len(courses) for courses in UNC_COURSES.values())} total courses")
        print(f"   - {total_submissions} class difficulty submissions")
        print(f"   - {total_ratings} professor ratings")
        print(f"   - {len(SAMPLE_PROFESSORS)} unique professors")
        
        # Test the data
        print(f"\n🔍 Testing database queries...")
        for major in list(UNC_COURSES.keys())[:3]:  # Test first 3 majors
            rankings = db_manager.get_class_rankings_by_major(major, limit=5)
            print(f"   - {major}: {len(rankings)} ranked classes")
        
        print(f"\n✅ StudySync is ready with realistic UNC course data!")
        print(f"🌐 You can now test the application with real course information.")
        
    except Exception as e:
        print(f"❌ Error during initialization: {e}")
        raise

if __name__ == "__main__":
    initialize_database()