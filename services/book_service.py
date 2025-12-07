# services/book_service.py
from typing import List, Optional, Dict, Any
from models import Book
from utils.sample_data import generate_sample_books
from utils.helpers import generate_id, calculate_progress
import json
import os


class BookService:
    def __init__(self, data_file: str = "books_data.json"):
        # ensure the data file path is inside project root (next to MAIN.py)
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        if not os.path.isabs(data_file):
            data_file = os.path.join(base_dir, data_file)
        self.data_file = os.path.abspath(data_file)

        self.books: List[Book] = []
        self.load_data()

    def load_data(self):
        """Load books from file or generate sample data"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                loaded = []
                # Accept either list of dicts or list of serialized book dicts
                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict):
                            try:
                                loaded.append(Book(**item))
                            except Exception:
                                # fallback: if keys mismatch, skip item
                                continue
                if not loaded:
                    # fallback to generating sample books
                    self.books = generate_sample_books(10)
                else:
                    self.books = loaded
            else:
                self.books = generate_sample_books(10)
        except Exception:
            # On any error, fall back to sample data
            self.books = generate_sample_books(10)

    def save_data(self):
        """Save books to file"""
        try:
            folder = os.path.dirname(self.data_file)
            if folder and not os.path.exists(folder):
                os.makedirs(folder, exist_ok=True)
            data = [book.to_dict() for book in self.books]
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: failed to save books data: {e}")

    def get_all_books(self) -> List[Book]:
        """Get all books"""
        return self.books

    # Backwards-compatible aliases for older component code
    def list_books(self) -> List[Book]:
        return self.get_all_books()

    def create_book(self, book_data: Dict[str, Any]) -> Book:
        return self.add_book(book_data)

    def get_book_by_id(self, book_id: str) -> Optional[Book]:
        """Get a book by its ID"""
        for book in self.books:
            if book.id == book_id:
                return book
        return None

    def add_book(self, book_data: Dict[str, Any]) -> Book:
        """Add a new book"""
        book = Book(
            id=generate_id(),
            **book_data
        )
        self.books.append(book)
        self.save_data()
        return book

    def update_book(self, book_id: str, updates: Dict[str, Any]) -> Optional[Book]:
        """Update an existing book"""
        for i, book in enumerate(self.books):
            if book.id == book_id:
                for key, value in updates.items():
                    if hasattr(book, key):
                        setattr(self.books[i], key, value)

                # Auto-calculate progress if pages are updated
                if 'current_page' in updates or 'total_pages' in updates:
                    self.books[i].progress = calculate_progress(
                        self.books[i].current_page,
                        self.books[i].total_pages
                    )

                self.save_data()
                return self.books[i]
        return None

    def delete_book(self, book_id: str) -> bool:
        """Delete a book"""
        initial_length = len(self.books)
        self.books = [book for book in self.books if book.id != book_id]
        if len(self.books) < initial_length:
            self.save_data()
            return True
        return False

    def search_books(self, query: str, filters: Dict[str, Any] = None) -> List[Book]:
        """Search books with optional filters"""
        query = query.lower().strip()
        filtered_books = self.books

        if query:
            filtered_books = [
                book for book in filtered_books
                if (query in book.title.lower() or
                    query in book.author.lower() or
                    query in book.genre.lower() or
                    query in book.isbn)
            ]

        if filters:
            if filters.get('status') and filters['status'] != 'All':
                filtered_books = [b for b in filtered_books if b.status == filters['status']]

            if filters.get('category') and filters['category'] != 'All':
                filtered_books = [b for b in filtered_books if filters['category'] in b.categories]

            if filters.get('min_rating', 0) > 0:
                filtered_books = [b for b in filtered_books if b.rating >= filters['min_rating']]

        return filtered_books

    def get_books_by_status(self, status: str) -> List[Book]:
        """Get books by reading status"""
        return [book for book in self.books if book.status == status]

    def get_books_by_category(self, category_name: str) -> List[Book]:
        """Get books by category"""
        return [book for book in self.books if category_name in book.categories]

    def update_book_status(self, book_id: str, status: str, current_page: int = None) -> Optional[Book]:
        """Update book reading status"""
        from datetime import datetime

        book = self.get_book_by_id(book_id)
        if not book:
            return None

        updates = {'status': status}

        if status == 'Reading' and not book.start_date:
            updates['start_date'] = datetime.now().strftime("%Y-%m-%d")
        elif status == 'Completed' and not book.finish_date:
            updates['finish_date'] = datetime.now().strftime("%Y-%m-%d")
            if book.total_pages > 0:
                updates['current_page'] = book.total_pages
                updates['progress'] = 100

        if current_page is not None:
            updates['current_page'] = current_page
            if book.total_pages > 0:
                updates['progress'] = calculate_progress(current_page, book.total_pages)

        return self.update_book(book_id, updates)

    def rate_book(self, book_id: str, rating: float, review: str = "") -> Optional[Book]:
        """Rate and review a book"""
        return self.update_book(book_id, {'rating': rating, 'review': review})

    def get_statistics(self) -> Dict[str, Any]:
        """Calculate book statistics"""
        if not self.books:
            return {
                'total_books': 0,
                'completed_books': 0,
                'reading_books': 0,
                'average_progress': 0,
                'total_pages': 0,
                'genres': {}
            }

        total_books = len(self.books)
        completed_books = len([b for b in self.books if b.status == 'Completed'])
        reading_books = len([b for b in self.books if b.status == 'Reading'])
        average_progress = sum(b.progress for b in self.books) / total_books
        total_pages = sum(b.total_pages for b in self.books)

        # Count genres
        genres = {}
        for book in self.books:
            for genre in book.genre.split(','):
                genre = genre.strip()
                genres[genre] = genres.get(genre, 0) + 1

        favorite_genre = max(genres.items(), key=lambda x: x[1])[0] if genres else "None"

        return {
            'total_books': total_books,
            'completed_books': completed_books,
            'reading_books': reading_books,
            'average_progress': round(average_progress, 1),
            'total_pages': total_pages,
            'favorite_genre': favorite_genre,
            'genres': genres
        }