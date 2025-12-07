# services/__init__.py
"""
Services package init — re-export service classes with safe imports.
"""
import sys
import os

# ensure project root is on sys.path when modules are imported as scripts
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# Safe imports with fallbacks to None so MAIN.py can handle missing services
try:
    from .book_service import BookService
except Exception as e:  # pragma: no cover
    BookService = None

try:
    from .category_service import CategoryService
except Exception as e:  # pragma: no cover
    CategoryService = None

try:
    from .stats_service import StatsService
except Exception as e:  # pragma: no cover
    StatsService = None

try:
    from .achievement_service import AchievementService
except Exception:
    AchievementService = None

# Exported singletons will be set at runtime by MAIN.py
book_service = None
category_service = None
stats_service = None
achievement_service = None

__all__ = ["book_service", "category_service", "stats_service", "achievement_service"]
