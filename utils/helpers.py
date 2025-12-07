"""Helper functions for Libris Core"""
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
    if not isinstance(text, str):
        text = str(text)
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
    if not isinstance(rating, (int, float)):
        rating = 0.0
    
    rating = max(0, min(5, rating))  # Clamp between 0 and 5
    
    full_stars = int(rating)
    half_star = 1 if rating - full_stars >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star

    stars = "★" * full_stars
    if half_star:
        stars += "½"
    stars += "☆" * empty_stars

    return stars


def format_date(date_str: str) -> str:
    """Format date string for display"""
    try:
        if not date_str:
            return "N/A"
        # Parse and reformat date
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%B %d, %Y")
    except:
        return date_str


def get_reading_time_estimate(pages: int, reading_speed: int = 250) -> int:
    """Estimate reading time in hours"""
    if pages <= 0 or reading_speed <= 0:
        return 0
    return int(pages / reading_speed)