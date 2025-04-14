"""generating multiple schedules in descending order based on calculated score"""

from itertools import product
# for combinations of sections/courses

def calculate_time_score(schedule, schedule_range: tuple): #2-tuple - dr.kong
    preferred_start, preferred_end = schedule_range
    score = 0
    for section in schedule:
        start = section['start']
        end = section['end']
        if preferred_start <= start and end <= preferred_end:
            score += 1  
        else:
            # take away from score, based on how far from schedule_range
            distance = max(0, preferred_start - start) + max(0, end - preferred_end)
            score -= distance * 0.1  # penalty factor. change later maybe
    return score

def calculate_prof_score(schedule, prof_ratings):
    return sum(prof_ratings.get(section['prof_id'], 0) for section in schedule)
    #.get defaults to 0 if rating not found
    # what to do if terrible prof and good time score and vice versa

def has_conflict(schedule):
    times = []
    for section in schedule:
        times.append((section['start'], section['end']))
    times.sort()
    for i in range(1, len(times)):
        if times[i][0] < times[i-1][1]:
            return True
    return False

def generate_schedules(schedule_range, course_list, prof_ratings, time_weight=1.0, prof_weight=1.0):
   # weights can be adjusted later
    all_combinations = product(*course_list)
    valid_schedules = []

    for combo in all_combinations:
        if has_conflict(combo):
            continue

        time_score = calculate_time_score(combo, schedule_range)
        prof_score = calculate_prof_score(combo, prof_ratings)
        total_score = time_weight * time_score + prof_weight * prof_score

        valid_schedules.append({
            'schedule': combo,
            'score': total_score
        })

    sorted_schedules = sorted(valid_schedules, key=lambda x: x['score'], reverse=True)
    return sorted_schedules
"""specify schedule data types"""
    