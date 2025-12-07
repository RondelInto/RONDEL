# utils/helpers.py
import random
from datetime import datetime
from typing import Any


def generate_id(prefix: str = "book") -> str:
    """Generate a unique ID"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_num = random.randint(1000, 9999)
    return f"{prefix}-{timestamp}-{random_num}"


def truncate_text(text: str, max_length: int = 50) -> str:
    """Truncate text with ellipsis if too long"""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def calculate_progress(current: int, total: int) -> int:
    """Calculate progress percentage"""
    if total == 0:
        return 0
    return min(100, int((current / total) * 100))


def get_star_rating(rating: float) -> str:
    """Convert numeric rating to star representation"""
    full_stars = int(rating)
    half_star = 1 if rating - full_stars >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star

    stars = "★" * full_stars
    if half_star:
        stars += "½"
    stars += "☆" * empty_stars

    return stars