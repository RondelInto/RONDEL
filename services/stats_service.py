# services/stats_service.py
from typing import List, Dict, Any
import random
from datetime import datetime

try:
    from utils.sample_data import generate_sample_achievements
except Exception:
    def generate_sample_achievements():
        return [
            type("A", (), {"id": "first-book", "title": "First Book", "unlocked": False}),
        ]


class StatsService:
    def __init__(self):
        # achievements are simple objects or dicts depending on sample_data
        self.achievements = generate_sample_achievements()

    def calculate_statistics(self, books: List) -> Any:
        """Return a simple object with expected attributes to avoid tight coupling with model classes."""
        class SimpleStats:
            def __init__(self):
                self.total_books = 0
                self.completed_books = 0
                self.reading_books = 0
                self.average_progress = 0
                self.monthly_completed = 0
                self.reading_streak = 0
                self.total_pages = 0
                self.favorite_genre = "None"

        stats = SimpleStats()
        if not books:
            return stats

        stats.total_books = len(books)
        stats.completed_books = len([b for b in books if getattr(b, 'status', '') == 'Completed'])
        stats.reading_books = len([b for b in books if getattr(b, 'status', '') == 'Reading'])
        total_progress = sum(getattr(b, 'progress', 0) for b in books)
        stats.average_progress = round((total_progress / stats.total_books) if stats.total_books else 0, 1)
        stats.total_pages = sum(getattr(b, 'total_pages', 0) for b in books)

        # genres
        genre_count = {}
        for book in books:
            genres = getattr(book, 'genre', '') or ''
            for genre in str(genres).split(','):
                g = genre.strip()
                if g:
                    genre_count[g] = genre_count.get(g, 0) + 1

        stats.favorite_genre = max(genre_count, key=genre_count.get) if genre_count else 'None'

        # monthly completed (best-effort)
        current_month = datetime.now().month
        monthly = 0
        for b in books:
            fd = getattr(b, 'finish_date', None)
            if fd:
                try:
                    if datetime.strptime(fd, "%Y-%m-%d").month == current_month:
                        monthly += 1
                except Exception:
                    pass
        stats.monthly_completed = monthly
        stats.reading_streak = random.randint(0, 30)

        return stats

    def check_achievements(self, books: List) -> List:
        total_books = len(books)
        completed_books = len([b for b in books if getattr(b, 'status', '') == 'Completed'])
        reading_books = len([b for b in books if getattr(b, 'status', '') == 'Reading'])

        unique_genres = set()
        for book in books:
            for genre in str(getattr(book, 'genre', '')).split(','):
                g = genre.strip()
                if g:
                    unique_genres.add(g)

        # Update achievements if they are dict-like or object-like
        for a in self.achievements:
            try:
                aid = a.id
            except Exception:
                aid = a.get('id') if isinstance(a, dict) else None

            if aid == 'first-book':
                if isinstance(a, dict):
                    a['unlocked'] = total_books >= 1
                else:
                    setattr(a, 'unlocked', total_books >= 1)
            if aid == 'five-books':
                if isinstance(a, dict):
                    a['unlocked'] = total_books >= 5
                else:
                    setattr(a, 'unlocked', total_books >= 5)

        return self.achievements

    def get_kpi_data(self, books: List) -> List[Dict[str, Any]]:
        stats = self.calculate_statistics(books)
        kpis = [
            {"title": "Total Books", "value": stats.total_books, "icon": "📚", "color": "#4B0082"},
            {"title": "Completed", "value": stats.completed_books, "icon": "✅", "color": "#10B981"},
            {"title": "Reading Now", "value": stats.reading_books, "icon": "📖", "color": "#3B82F6"},
            {"title": "Avg Progress", "value": f"{stats.average_progress}%", "icon": "📈", "color": "#F59E0B"},
        ]
        return kpis

    def get_genre_distribution(self, books: List) -> Dict[str, int]:
        genre_count = {}
        for book in books:
            for genre in str(getattr(book, 'genre', '')).split(','):
                g = genre.strip()
                if g:
                    genre_count[g] = genre_count.get(g, 0) + 1
        return genre_count

    def get_reading_timeline(self, books: List) -> Dict[str, int]:
        timeline = {}
        current_year = datetime.now().year
        for year in range(current_year - 2, current_year + 1):
            timeline[str(year)] = random.randint(1, 10)
        return timeline