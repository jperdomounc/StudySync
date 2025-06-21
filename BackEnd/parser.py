"""parse shopping cart"""
import re
from typing import List
from models import Course

def parse_shopping_cart(text: str) -> List[Course]:
    lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
    courses = []
    i = 0

    while i < len(lines) - 6:
        # Start of course entry
        if re.match(r"^[A-Z]{2,} \d{3}-\d{3}$", lines[i]):
            # Safely get next lines assuming structure
            try:
                class_code = lines[i]
                days_times = lines[i + 2]
                location = lines[i + 3]
                instructor = lines[i + 4]
                units = lines[i + 5]
                # We skip Status line (i + 6)

                days, start_time, end_time = parse_schedule(days_times)

                courses.append(Course(
                    title=class_code,
                    instructor=instructor if "To be Announced" not in instructor else "TBA",
                    days=days,
                    start_time=start_time,
                    end_time=end_time,
                    rating=None
                ))
                i += 7  # Skip to next course
            except IndexError:
                break  # end of list
        else:
            i += 1  # not a valid course line

    return courses

def parse_schedule(line: str):
    """Converts 'MoWeFr 8:00AM - 8:50AM' -> ['Mon', 'Wed', 'Fri'], '08:00', '08:50'"""
    match = re.match(r'^([A-Za-z]+) (\d{1,2}:\d{2}[APMapm]+) - (\d{1,2}:\d{2}[APMapm]+)$', line)
    if not match:
        return [], "00:00", "00:00"
    day_part, start, end = match.groups()
    days = parse_days(day_part)
    return days, _normalize_time(start), _normalize_time(end)

def parse_days(day_str: str) -> List[str]:
    # Map abbreviations to full weekday names
    day_map = {
        "Mo": "Mon", "Tu": "Tue", "We": "Wed", "Th": "Thu", "Fr": "Fri"
    }
    return [day_map[d] for d in re.findall(r'Mo|Tu|We|Th|Fr', day_str)]

def _normalize_time(t: str) -> str:
    from datetime import datetime
    return datetime.strptime(t.strip().upper(), "%I:%M%p").strftime("%H:%M")
