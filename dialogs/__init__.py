"""Dialog components package for Libris Core - minimal init to avoid circular imports.

Import specific dialogs where needed, e.g.:
  from components.dialogs.book_details import BookDetailsDialog
"""
# try to import public dialog symbols; fall back to None to avoid import-time circular errors
try:
    from .book_details import BookDetailsDialog
    from .category_editor import CategoryEditorDialog
    from .rate_review import RateReviewDialog
    from .search_results import SearchResultsDialog
    from .track_progress import TrackProgressDialog
except Exception:
    BookDetailsDialog = None
    CategoryEditorDialog = None
    RateReviewDialog = None
    SearchResultsDialog = None
    TrackProgressDialog = None

__all__ = [
    "BookDetailsDialog",
    "CategoryEditorDialog",
    "RateReviewDialog",
    "SearchResultsDialog",
    "TrackProgressDialog",
]