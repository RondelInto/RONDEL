"""Achievement service: small helper to compute earned achievements."""
from typing import List, Dict, Any
try:
	from utils.sample_data import generate_sample_achievements
except Exception:
	def generate_sample_achievements():
		return [
			{"id": "first-book", "title": "First Book", "unlocked": False},
			{"id": "five-books", "title": "5 Books", "unlocked": False},
		]


class AchievementService:
	def __init__(self, book_service=None):
		self.book_service = book_service
		self.achievements = generate_sample_achievements()

	def get_achievements(self) -> List[Dict[str, Any]]:
		if not self.book_service:
			return self.achievements
		total = len(self.book_service.get_all_books())
		for a in self.achievements:
			if a.get("id") == "first-book":
				a["unlocked"] = total >= 1
			if a.get("id") == "five-books":
				a["unlocked"] = total >= 5
		return self.achievements
