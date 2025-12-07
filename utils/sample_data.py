# utils/sample_data.py
import random
from datetime import datetime, timedelta
from models import Book, Category, Achievement
from utils.helpers import generate_id


def generate_sample_books(count: int = 10) -> list:
    """Generate sample books for testing"""
    books = []

    sample_books_data = [
        {
            "title": "The Great Gatsby",
            "author": "F. Scott Fitzgerald",
            "publisher": "Scribner",
            "genre": "Classic, Fiction",
            "isbn": "9780743273565",
            "year": 1925,
            "description": "A classic novel of the Jazz Age, telling the tragic story of self-made millionaire Jay Gatsby and his pursuit of the beautiful Daisy Buchanan.",
            "total_pages": 180
        },
        {
            "title": "To Kill a Mockingbird",
            "author": "Harper Lee",
            "publisher": "J. B. Lippincott & Co.",
            "genre": "Classic, Fiction, Historical",
            "isbn": "9780446310789",
            "year": 1960,
            "description": "The unforgettable novel of a childhood in a sleepy Southern town and the crisis of conscience that rocked it.",
            "total_pages": 281
        },
        {
            "title": "1984",
            "author": "George Orwell",
            "publisher": "Secker & Warburg",
            "genre": "Dystopian, Political Fiction",
            "isbn": "9780451524935",
            "year": 1949,
            "description": "A dystopian social science fiction novel and cautionary tale about the dangers of totalitarianism.",
            "total_pages": 328
        },
        {
            "title": "Pride and Prejudice",
            "author": "Jane Austen",
            "publisher": "T. Egerton",
            "genre": "Classic, Romance",
            "isbn": "9780141439518",
            "year": 1813,
            "description": "The romantic clash between the opinionated Elizabeth and her proud beau, Mr. Darcy, is a splendid performance of civilized sparring.",
            "total_pages": 432
        },
        {
            "title": "The Hobbit",
            "author": "J.R.R. Tolkien",
            "publisher": "George Allen & Unwin",
            "genre": "Fantasy, Adventure",
            "isbn": "9780547928227",
            "year": 1937,
            "description": "Bilbo Baggins, a respectable, well-to-do hobbit, lives comfortably in his hobbit-hole until the day the wandering wizard Gandalf chooses him to take part in an adventure.",
            "total_pages": 310
        }
    ]

    statuses = ["Not Started", "Reading", "Completed", "On Hold"]

    for i in range(min(count, len(sample_books_data))):
        book_data = sample_books_data[i % len(sample_books_data)]
        status = statuses[i % len(statuses)]

        # Generate dates based on status
        start_date = ""
        finish_date = ""
        current_page = 0
        progress = 0

        if status == "Reading":
            start_date = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d")
            current_page = random.randint(1, book_data["total_pages"] // 2)
            progress = int((current_page / book_data["total_pages"]) * 100)
        elif status == "Completed":
            start_date = (datetime.now() - timedelta(days=random.randint(60, 365))).strftime("%Y-%m-%d")
            finish_date = (datetime.now() - timedelta(days=random.randint(1, 59))).strftime("%Y-%m-%d")
            current_page = book_data["total_pages"]
            progress = 100

        book = Book(
            id=generate_id(),
            title=book_data["title"],
            author=book_data["author"],
            publisher=book_data["publisher"],
            genre=book_data["genre"],
            isbn=book_data["isbn"],
            year=book_data["year"],
            status=status,
            progress=progress,
            current_page=current_page,
            total_pages=book_data["total_pages"],
            rating=random.uniform(3.5, 5.0) if status == "Completed" else 0.0,
            review="A wonderful read!" if status == "Completed" and random.random() > 0.5 else "",
            categories=["General"] + (["Favorites"] if i < 2 else []),
            description=book_data["description"],
            start_date=start_date,
            finish_date=finish_date,
            notes="Great book!" if status == "Completed" else ""
        )

        books.append(book)

    return books


def generate_sample_categories() -> list:
    """Generate sample categories"""
    categories = [
        Category(name="Favorites", color="#4B0082"),
        Category(name="Want to Read", color="#10B981"),
        Category(name="Currently Reading", color="#3B82F6"),
        Category(name="Classics", color="#F59E0B"),
        Category(name="Science Fiction", color="#EF4444"),
        Category(name="Non-Fiction", color="#7A3BA3"),
        Category(name="Fantasy", color="#8B5CF6"),
        Category(name="Biography", color="#EC4899")
    ]
    return categories


def generate_sample_achievements() -> list:
    """Generate sample achievements"""
    achievements = [
        Achievement(id="first-book", name="First Book", description="Add your first book to the library", icon="📚"),
        Achievement(id="five-books", name="Book Collector", description="Add 5 books to your library", icon="⭐"),
        Achievement(id="ten-books", name="Library Builder", description="Add 10 books to your library", icon="🏆"),
        Achievement(id="week-streak", name="Reading Streak", description="Maintain a 7-day reading streak", icon="🔥"),
        Achievement(id="multitasker", name="Multitasker", description="Read 3 books simultaneously", icon="📖"),
        Achievement(id="dedicated-reader", name="Dedicated Reader", description="Complete 5 books", icon="💪"),
        Achievement(id="speed-reader", name="Speed Reader", description="Complete a book in 3 days", icon="⚡"),
        Achievement(id="genre-master", name="Genre Master", description="Read books from 5 different genres", icon="🎭")
    ]
    return achievements