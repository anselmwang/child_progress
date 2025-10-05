import re
from typing import List, Tuple, Optional

def extract_alcumus_timestamps(text: str) -> List[str]:
    """
    Extract Alcumus problem timestamps from pasted text.
    
    Args:
        text: Pasted text from AOPS Alcumus page
    
    Returns:
        List of timestamps found (format: YYYY-MM-DD HH:MM:SS)
    """
    # Pattern to match timestamps like "2025-09-01 12:45:52"
    timestamp_pattern = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}'
    timestamps = re.findall(timestamp_pattern, text)
    return timestamps


def parse_problem_number(problem_str: str) -> Optional[Tuple[int, int, Optional[int]]]:
    """
    Parse AOPS problem number into components.
    
    Args:
        problem_str: String like "15.1" (Problem) or "15.1.5" (Exercise)
    
    Returns:
        Tuple of (chapter, section, exercise_num) or None if invalid
        exercise_num is None for Problems
    """
    problem_str = problem_str.strip()
    
    # Problem format: X.Y (exactly one dot)
    problem_pattern = r'^(\d+)\.(\d+)$'
    problem_match = re.match(problem_pattern, problem_str)
    if problem_match:
        chapter = int(problem_match.group(1))
        section = int(problem_match.group(2))
        return (chapter, section, None)
    
    # Exercise format: X.Y.Z (exactly two dots)
    exercise_pattern = r'^(\d+)\.(\d+)\.(\d+)$'
    exercise_match = re.match(exercise_pattern, problem_str)
    if exercise_match:
        chapter = int(exercise_match.group(1))
        section = int(exercise_match.group(2))
        exercise = int(exercise_match.group(3))
        return (chapter, section, exercise)
    
    return None


def validate_problem_format(problems_str: str) -> Tuple[bool, str, List[str], List[str]]:
    """
    Validate and parse comma-separated problem numbers.
    
    Returns:
        (is_valid, error_message, problems_list, exercises_list)
    """
    if not problems_str.strip():
        return True, "", [], []
    
    # Split by comma and clean up
    items = [item.strip() for item in problems_str.split(',') if item.strip()]
    
    problems = []
    exercises = []
    
    for item in items:
        parsed = parse_problem_number(item)
        if parsed is None:
            return False, f"无效格式: '{item}'. 请使用格式 X.Y (问题) 或 X.Y.Z (练习)", [], []
        
        chapter, section, exercise_num = parsed
        if exercise_num is None:
            # This is a Problem
            problems.append(item)
        else:
            # This is an Exercise
            exercises.append(item)
    
    return True, "", problems, exercises


def is_consecutive_problems(prob1: str, prob2: str) -> bool:
    """Check if two problems are consecutive."""
    parsed1 = parse_problem_number(prob1)
    parsed2 = parse_problem_number(prob2)
    
    if not parsed1 or not parsed2:
        return False
    
    ch1, sec1, ex1 = parsed1
    ch2, sec2, ex2 = parsed2
    
    # Both must be same type (Problem or Exercise)
    if (ex1 is None) != (ex2 is None):
        return False
    
    if ex1 is None and ex2 is None:
        # Both are Problems
        if ch1 == ch2:
            return sec2 == sec1 + 1
        else:
            # Cross-chapter: assume chapter transition is valid
            return ch2 == ch1 + 1 and sec2 == 1
    else:
        # Both are Exercises
        if ch1 == ch2 and sec1 == sec2:
            return ex2 == ex1 + 1
        elif ch1 == ch2 and sec2 == sec1 + 1:
            # Cross-section within same chapter
            return ex2 == 1
        elif ch2 == ch1 + 1:
            # Cross-chapter
            return sec2 == 1 and ex2 == 1
        else:
            return False


def validate_daily_continuity(items: List[str]) -> Tuple[bool, str]:
    """Validate that items within the same day are consecutive."""
    if len(items) <= 1:
        return True, ""
    
    for i in range(len(items) - 1):
        if not is_consecutive_problems(items[i], items[i + 1]):
            return False, f"题目不连续: {items[i]} 到 {items[i + 1]}"
    
    return True, ""


def validate_cross_day_continuity(today_items: List[str], 
                                yesterday_items: List[str]) -> Tuple[bool, str]:
    """Validate continuity between yesterday's last item and today's first item."""
    if not today_items or not yesterday_items:
        return True, ""
    
    today_first = today_items[0]
    yesterday_last = yesterday_items[-1]
    
    if not is_consecutive_problems(yesterday_last, today_first):
        return False, f"跨天不连续: 昨天最后题目 {yesterday_last}, 今天第一题 {today_first}"
    
    return True, ""


def validate_continuity(today_problems: List[str], today_exercises: List[str],
                       previous_problems: List[str], previous_exercises: List[str]) -> Tuple[bool, str]:
    """
    Complete continuity validation for a day's progress.
    
    Returns:
        (is_valid, error_message)
    """
    # Validate daily continuity for problems
    if today_problems:
        valid, error = validate_daily_continuity(today_problems)
        if not valid:
            return False, f"Problem连续性错误: {error}"
    
    # Validate daily continuity for exercises
    if today_exercises:
        valid, error = validate_daily_continuity(today_exercises)
        if not valid:
            return False, f"Exercise连续性错误: {error}"
    
    # Validate cross-day continuity for problems
    if today_problems and previous_problems:
        valid, error = validate_cross_day_continuity(today_problems, previous_problems)
        if not valid:
            return False, f"Problem {error}"
    
    # Validate cross-day continuity for exercises
    if today_exercises and previous_exercises:
        valid, error = validate_cross_day_continuity(today_exercises, previous_exercises)
        if not valid:
            return False, f"Exercise {error}"
    
    return True, ""
