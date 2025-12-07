"""Data models for Libris Core"""
from dataclasses import dataclass, field
from typing import List
import inspect


@dataclass
class Book:
    id: str
    title: str
    author: str
    publisher: str
    genre: str
    isbn: str
    year: int
    status: str = "Not Started"
    progress: int = 0
    current_page: int = 0
    total_pages: int = 0
    rating: float = 0.0
    review: str = ""
    categories: List[str] = field(default_factory=lambda: ["General"])
    cover_image: str = ""
    description: str = ""
    start_date: str = ""
    finish_date: str = ""
    notes: str = ""

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "publisher": self.publisher,
            "genre": self.genre,
            "isbn": self.isbn,
            "year": self.year,
            "status": self.status,
            "progress": self.progress,
            "current_page": self.current_page,
            "total_pages": self.total_pages,
            "rating": self.rating,
            "review": self.review,
            "categories": self.categories,
            "cover_image": self.cover_image,
            "description": self.description,
            "start_date": self.start_date,
            "finish_date": self.finish_date,
            "notes": self.notes
        }

    @classmethod
    def from_dict(cls, data):
        """Create Book instance from dictionary in a tolerant way."""
        # build kwargs only from known dataclass fields, using defaults when missing
        fields = cls.__dataclass_fields__
        kwargs = {}
        for fname, meta in fields.items():
            if fname in data and data[fname] is not None:
                val = data[fname]
                # try some safe coercions for common numeric fields
                if fname in ("year", "progress", "current_page", "total_pages"):
                    try:
                        val = int(val)
                    except Exception:
                        # fallback to 0 if conversion fails
                        val = 0
                if fname == "rating":
                    try:
                        val = float(val)
                    except Exception:
                        val = 0.0
                kwargs[fname] = val
            else:
                # use default if provided, otherwise skip to let dataclass apply default
                if meta.default is not inspect._empty:
                    kwargs[fname] = meta.default
                elif meta.default_factory is not inspect._empty:  # type: ignore[attr-defined]
                    kwargs[fname] = meta.default_factory()  # type: ignore[misc]
        try:
            return cls(**kwargs)
        except Exception:
            # last resort: try to construct with minimal required fields with safe defaults
            minimal = {
                "id": data.get("id", ""),
                "title": data.get("title", "Untitled"),
                "author": data.get("author", "Unknown"),
                "publisher": data.get("publisher", ""),
                "genre": data.get("genre", ""),
                "isbn": data.get("isbn", ""),
                "year": int(data.get("year", 0) or 0),
            }
            return cls(**minimal)


@dataclass
class Category:
    name: str
    color: str
    book_count: int = 0

    def to_dict(self):
        return {
            "name": self.name,
            "color": self.color,
            "book_count": self.book_count
        }

    @classmethod
    def from_dict(cls, data):
        """Create Category instance from dictionary (tolerant)."""
        fields = cls.__dataclass_fields__
        kwargs = {}
        for fname, meta in fields.items():
            if fname in data and data[fname] is not None:
                kwargs[fname] = data[fname]
            else:
                if meta.default is not inspect._empty:
                    kwargs[fname] = meta.default
                elif meta.default_factory is not inspect._empty:  # type: ignore[attr-defined]
                    kwargs[fname] = meta.default_factory()  # type: ignore[misc]
        try:
            return cls(**kwargs)
        except Exception:
            return cls(name=str(data.get("name", "General")), color=str(data.get("color", "#cccccc")), book_count=int(data.get("book_count", 0)))


@dataclass
class Achievement:
    id: str
    name: str
    description: str
    unlocked: bool = False
    icon: str = "🏆"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "unlocked": self.unlocked,
            "icon": self.icon
        }


@dataclass
class Statistics:
    total_books: int = 0
    completed_books: int = 0
    reading_books: int = 0
    average_progress: float = 0.0
    monthly_completed: int = 0
    reading_streak: int = 0
    total_pages: int = 0
    favorite_genre: str = ""

    def to_dict(self):
        return {
            "total_books": self.total_books,
            "completed_books": self.completed_books,
            "reading_books": self.reading_books,
            "average_progress": self.average_progress,
            "monthly_completed": self.monthly_completed,
            "reading_streak": self.reading_streak,
            "total_pages": self.total_pages,
            "favorite_genre": self.favorite_genre
        }