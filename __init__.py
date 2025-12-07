# components/__init__.py
"""Components package for Libris Core - safe imports to avoid import-time crashes."""
# try to import each component; if a module fails to import, expose None so callers can handle missing pieces.

try:
    from .header import Header
except Exception as e:
    print(f"Warning: Could not import Header: {e}")
    Header = None

try:
    from .library_tab import LibraryTab
except Exception as e:
    print(f"Warning: Could not import LibraryTab: {e}")
    LibraryTab = None

try:
    from .stats_tab import StatsTab
except Exception as e:
    print(f"Warning: Could not import StatsTab: {e}")
    StatsTab = None

try:
    from .categories_tab import CategoriesTab
except Exception as e:
    print(f"Warning: Could not import CategoriesTab: {e}")
    CategoriesTab = None

try:
    from .add_book_tab import AddBookTab
except Exception as e:
    print(f"Warning: Could not import AddBookTab: {e}")
    AddBookTab = None

try:
    from .search_tab import SearchTab
except Exception as e:
    print(f"Warning: Could not import SearchTab: {e}")
    SearchTab = None

__all__ = [
    'Header',
    'LibraryTab',
    'StatsTab',
    'CategoriesTab',
    'AddBookTab',
    'SearchTab'
]
