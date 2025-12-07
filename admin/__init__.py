"""Admin components package for Libris Core"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

try:
    from .admin_dashboard import AdminDashboard
except ImportError as e:
    print(f"Warning: Could not import AdminDashboard: {e}")
    AdminDashboard = None

try:
    from .admin_header import AdminHeader
except ImportError as e:
    print(f"Warning: Could not import AdminHeader: {e}")
    AdminHeader = None

try:
    from .admin_tabs import AdminTabBar
except ImportError as e:
    print(f"Warning: Could not import AdminTabBar: {e}")
    AdminTabBar = None

try:
    from .admin_tabs_content import (
        BooksTab, UsersTab, TransactionsTab,
        KPITab, ReportsTab, SystemTab
    )
except ImportError as e:
    print(f"Warning: Could not import tab content: {e}")
    BooksTab = UsersTab = TransactionsTab = None
    KPITab = ReportsTab = SystemTab = None

try:
    from .kpi_cards import KPICard, KPICardsGrid
except ImportError as e:
    print(f"Warning: Could not import KPI cards: {e}")
    KPICard = KPICardsGrid = None

__all__ = [
    'AdminDashboard',
    'AdminHeader',
    'AdminTabBar',
    'BooksTab',
    'UsersTab',
    'TransactionsTab',
    'KPITab',
    'ReportsTab',
    'SystemTab',
    'KPICard',
    'KPICardsGrid'
]