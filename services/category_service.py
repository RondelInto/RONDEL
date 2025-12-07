# services/category_service.py
from typing import List, Optional, Dict, Any
import json
import os
import datetime

try:
    from models import Category
except Exception:
    # Minimal fallback Category model
    class Category:
        def __init__(self, name: str, color: str = "#dddddd", book_count: int = 0, created_at: str = None):
            self.name = name
            self.color = color
            self.book_count = book_count
            self.created_at = created_at or datetime.datetime.utcnow().isoformat()

        def to_dict(self):
            return {"name": self.name, "color": self.color, "book_count": self.book_count, "created_at": self.created_at}

        @staticmethod
        def from_dict(d):
            return Category(d.get("name", ""), d.get("color", "#dddddd"), d.get("book_count", 0), d.get("created_at"))

try:
    from utils.sample_data import generate_sample_categories
except Exception:
    def generate_sample_categories():
        return [Category(name=n) for n in ["General", "Fiction", "Non-Fiction"]]


class CategoryService:
    def __init__(self, data_file: str = "categories_data.json"):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        if not os.path.isabs(data_file):
            data_file = os.path.join(base_dir, data_file)
        self.data_file = os.path.abspath(data_file)
        self.categories: List[Category] = []
        self.load_data()

    def load_data(self):
        """Load categories from file or generate sample data"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.categories = []
                if isinstance(data, list):
                    for item in data:
                        try:
                            if isinstance(item, dict) and hasattr(Category, 'from_dict'):
                                self.categories.append(Category.from_dict(item))
                            elif isinstance(item, dict):
                                self.categories.append(Category(**item))
                        except Exception:
                            continue
                if not self.categories:
                    self.categories = generate_sample_categories()
            else:
                self.categories = generate_sample_categories()
        except Exception:
            self.categories = generate_sample_categories()

    def save_data(self):
        """Save categories to file"""
        try:
            folder = os.path.dirname(self.data_file)
            if folder and not os.path.exists(folder):
                os.makedirs(folder, exist_ok=True)
            data = [c.to_dict() if hasattr(c, 'to_dict') else {'name': c.name, 'color': c.color, 'book_count': getattr(c, 'book_count', 0)} for c in self.categories]
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: could not save categories data: {e}")

    def get_all_categories(self) -> List[Category]:
        """Get all categories"""
        return self.categories

    def get_category_by_name(self, name: str) -> Optional[Category]:
        """Get a category by name"""
        for category in self.categories:
            if category.name == name:
                return category
        return None

    def create_category(self, name: str, color: str) -> Optional[Category]:
        """Create a new category"""
        # Check if category already exists
        if any(cat.name.lower() == name.lower() for cat in self.categories):
            return None

        category = Category(name=name, color=color)
        self.categories.append(category)
        self.save_data()
        return category

    def update_category(self, old_name: str, new_name: str, color: str) -> Optional[Category]:
        """Update an existing category"""
        for i, category in enumerate(self.categories):
            if category.name == old_name:
                # Check if new name conflicts with existing categories
                if new_name != old_name and any(cat.name.lower() == new_name.lower() for cat in self.categories):
                    return None

                self.categories[i].name = new_name
                self.categories[i].color = color
                self.save_data()
                return self.categories[i]
        return None

    def delete_category(self, name: str) -> bool:
        """Delete a category"""
        initial_length = len(self.categories)
        self.categories = [cat for cat in self.categories if cat.name != name]
        if len(self.categories) < initial_length:
            self.save_data()
            return True
        return False

    def update_book_counts(self, book_service) -> None:
        """Update book counts for all categories"""
        # Reset all counts
        for category in self.categories:
            category.book_count = 0

        # Count books in each category
        for book in book_service.get_all_books():
            for category_name in book.categories:
                category = self.get_category_by_name(category_name)
                if category:
                    category.book_count += 1

    def get_category_stats(self) -> Dict[str, Any]:
        """Get category statistics"""
        total_categories = len(self.categories)
        total_books_in_categories = sum(cat.book_count for cat in self.categories)

        # Get top categories
        sorted_categories = sorted(self.categories, key=lambda x: x.book_count, reverse=True)
        top_categories = [(cat.name, cat.book_count) for cat in sorted_categories[:5]]

        return {
            'total_categories': total_categories,
            'total_books_in_categories': total_books_in_categories,
            'top_categories': top_categories
        }