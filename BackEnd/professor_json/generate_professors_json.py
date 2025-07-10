import json
import re
from collections import defaultdict

INPUT_FILE = "biol_prof.txt"
OUTPUT_FILE = "biol_professors.json"

def extract_professors(text):
    prof_courses = defaultdict(list)

    lines = text.strip().splitlines()

    # Skip the header row if it exists
    for line in lines:
        line = line.strip()
        if not line or "Instructor" in line or "Section" in line:
            continue

        # Match course code (e.g., CHEM 101 001) and instructor
        match = re.match(r"([A-Z]{4}\s+\d{3}[A-Z]?\s+\d{3})\s+(.+)", line)
        if match:
            course = match.group(1).strip()
            name = match.group(2).strip()

            # Normalize: remove (Primary) or multiple spaces
            name = re.sub(r"\s*\(Primary\)", "", name).strip()
            name = re.sub(r"\s{2,}", " ", name)

            if name.lower() != "staff":
                prof_courses[name].append(course)

    # Build structured data
    professor_list = []
    for prof_name, courses in prof_courses.items():
        department = courses[0].split()[0] if courses else "UNKNOWN"
        professor_list.append({
            "name": prof_name,
            "department": department,
            "courses": courses,
            "rating": None,
            "difficulty": None,
            "wouldTakeAgain": None
        })

    return professor_list

def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        raw_text = f.read()

    data = extract_professors(raw_text)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        json.dump(data, out, indent=2)
        print(f"✅ Saved {len(data)} professors to '{OUTPUT_FILE}'")

if __name__ == "__main__":
    main()
