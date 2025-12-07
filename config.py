"""Configuration for Libris Core"""

# Color Palette
COLORS = {
    "primary": "#4B0082",
    "primary_dark": "#3A0066",
    "primary_light": "#6A0DAD",
    "secondary": "#7A3BA3",
    "accent": "#A67AC7",
    "light": "#D4B8E8",
    "background": "#f5f5f5",
    "card": "#ffffff",
    "text": "#333333",
    "text_light": "#666666",
    "success": "#10B981",
    "warning": "#F59E0B",
    "danger": "#EF4444",
    "info": "#3B82F6",
    "light_bg": "#fafafa",
    "border": "#e0e0e0",
    "dark": "#1A1A1A",
    "white": "#FFFFFF"
}

# Status Configuration
STATUS_COLORS = {
    "Reading": "#3B82F6",
    "Completed": "#10B981",
    "On Hold": "#F59E0B",
    "Not Started": "#D4B8E8"
}

STATUS_ICONS = {
    "Reading": "📖",
    "Completed": "✅",
    "On Hold": "⏸️",
    "Not Started": "📚"
}

# Database Configuration
DATABASE_FILE = "books_data.json"
CATEGORIES_FILE = "data/categories.json"
STATS_FILE = "data/stats.json"

# Application Configuration
APP_TITLE = "Libris Core"
APP_VERSION = "1.0.0"
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 800

# Admin Configuration
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# User Configuration
DEFAULT_USERNAME = "user"
DEFAULT_PASSWORD = "user123"

# Pagination
ITEMS_PER_PAGE = 20