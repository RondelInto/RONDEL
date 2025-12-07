# utils/validators.py
"""Validation functions for Libris Core"""
import re
from datetime import datetime
from typing import Optional, Tuple


def validate_isbn(isbn: str) -> Tuple[bool, str]:
    """Validate ISBN-13 format"""
    isbn = isbn.replace("-", "").replace(" ", "")
    
    if not isbn.isdigit():
        return False, "ISBN must contain only numbers"
    
    if len(isbn) != 13:
        return False, "ISBN must be 13 digits"
    
    # Calculate checksum
    total = sum(int(digit) * (1 if i % 2 == 0 else 3) for i, digit in enumerate(isbn[:12]))
    check_digit = (10 - (total % 10)) % 10
    
    if int(isbn[12]) == check_digit:
        return True, "Valid ISBN"
    else:
        return False, "Invalid ISBN checksum"


def validate_year(year: str) -> Tuple[bool, str]:
    """Validate publication year"""
    try:
        year_int = int(year)
        if year_int < 1000 or year_int > 2100:
            return False, "Year must be between 1000 and 2100"
        return True, "Valid year"
    except ValueError:
        return False, "Year must be a valid number"


def validate_pages(current_page: str, total_pages: str) -> Tuple[bool, str]:
    """Validate page numbers"""
    try:
        current = int(current_page) if current_page else 0
        total = int(total_pages) if total_pages else 1
        
        if current < 0:
            return False, "Current page cannot be negative"
        
        if total <= 0:
            return False, "Total pages must be greater than 0"
        
        if current > total:
            return False, f"Current page ({current}) cannot exceed total pages ({total})"
        
        return True, "Valid pages"
    except ValueError:
        return False, "Pages must be valid numbers"


def validate_rating(rating: str) -> Tuple[bool, str]:
    """Validate book rating"""
    try:
        rating_float = float(rating)
        if rating_float < 0 or rating_float > 5:
            return False, "Rating must be between 0 and 5"
        return True, "Valid rating"
    except ValueError:
        return False, "Rating must be a valid number"


def validate_book_title(title: str) -> Tuple[bool, str]:
    """Validate book title"""
    if not title or not title.strip():
        return False, "Title cannot be empty"
    
    if len(title) > 200:
        return False, "Title cannot exceed 200 characters"
    
    return True, "Valid title"


def validate_author(author: str) -> Tuple[bool, str]:
    """Validate author name"""
    if not author or not author.strip():
        return False, "Author cannot be empty"
    
    if len(author) > 100:
        return False, "Author name cannot exceed 100 characters"
    
    return True, "Valid author"


def validate_email(email: str) -> Tuple[bool, str]:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if re.match(pattern, email):
        return True, "Valid email"
    else:
        return False, "Invalid email format"