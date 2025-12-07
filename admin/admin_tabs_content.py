"""Admin Dashboard Tab Content Areas"""
import tkinter as tk
from tkinter import ttk, font
import sys
import os
import tkinter as tk
import sys
import os
from tkinter import ttk, font

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

try:
    from styles.admin_theme import (
        BLACK, DARK_GRAY, WHITE, LIGHT_GRAY,
        SPACING_32, SPACING_16, H2_SIZE, BODY_REGULAR
    )
except ImportError:
    BLACK = "#000000"
    DARK_GRAY = "#1A1A1A"
    WHITE = "#FFFFFF"
    LIGHT_GRAY = "#BFBFBF"
    SPACING_32 = 32
    SPACING_16 = 16
    H2_SIZE = 24
    BODY_REGULAR = 14


class AdminTabContent(tk.Frame):
    """Base class for tab content"""
    def __init__(self, parent, title, **kwargs):
        super().__init__(parent, bg=BLACK, **kwargs)
        self.title = title
        self._create_header()
    
    def _create_header(self):
        """Create tab header"""
        try:
            header = tk.Frame(self, bg=BLACK)
            header.pack(fill=tk.X, padx=SPACING_32, pady=(SPACING_32, SPACING_16))
            
            title_font = font.Font(family="Segoe UI", size=H2_SIZE, weight="bold")
            title_label = tk.Label(header, text=self.title, font=title_font, 
                                  fg=WHITE, bg=BLACK)
            title_label.pack(anchor="w")
        except Exception as e:
            print(f"Error creating header: {e}")


class BooksTab(AdminTabContent):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, "📚 Books Management", **kwargs)
        self._create_content()
    
    def _create_content(self):
        """Create books tab content"""
        content = tk.Frame(self, bg=BLACK)
        content.pack(fill=tk.BOTH, expand=True, padx=SPACING_32, pady=SPACING_16)
        
        # Placeholder content
        placeholder = tk.Label(content, text="Books management interface coming soon...", 
                              font=("Segoe UI", BODY_REGULAR), fg=LIGHT_GRAY, bg=BLACK)
        placeholder.pack(pady=SPACING_32)


class UsersTab(AdminTabContent):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, "👥 Users Management", **kwargs)
        self._create_content()
    
    def _create_content(self):
        """Create users tab content"""
        content = tk.Frame(self, bg=BLACK)
        content.pack(fill=tk.BOTH, expand=True, padx=SPACING_32, pady=SPACING_16)
        
        placeholder = tk.Label(content, text="Users management interface coming soon...", 
                              font=("Segoe UI", BODY_REGULAR), fg=LIGHT_GRAY, bg=BLACK)
        placeholder.pack(pady=SPACING_32)


class TransactionsTab(AdminTabContent):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, "💱 Transactions Log", **kwargs)
        self._create_content()
    
    def _create_content(self):
        """Create transactions tab content"""
        content = tk.Frame(self, bg=BLACK)
        content.pack(fill=tk.BOTH, expand=True, padx=SPACING_32, pady=SPACING_16)
        
        placeholder = tk.Label(content, text="Transactions log interface coming soon...", 
                              font=("Segoe UI", BODY_REGULAR), fg=LIGHT_GRAY, bg=BLACK)
        placeholder.pack(pady=SPACING_32)


class KPITab(AdminTabContent):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, "📊 KPI Dashboard", **kwargs)
        self._create_content()
    
    def _create_content(self):
        """Create KPI tab content"""
        content = tk.Frame(self, bg=BLACK)
        content.pack(fill=tk.BOTH, expand=True, padx=SPACING_32, pady=SPACING_16)
        
        placeholder = tk.Label(content, text="Advanced KPI metrics coming soon...", 
                              font=("Segoe UI", BODY_REGULAR), fg=LIGHT_GRAY, bg=BLACK)
        placeholder.pack(pady=SPACING_32)


class ReportsTab(AdminTabContent):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, "📄 Reports", **kwargs)
        self._create_content()
    
    def _create_content(self):
        """Create reports tab content"""
        content = tk.Frame(self, bg=BLACK)
        content.pack(fill=tk.BOTH, expand=True, padx=SPACING_32, pady=SPACING_16)
        
        placeholder = tk.Label(content, text="Report generation interface coming soon...", 
                              font=("Segoe UI", BODY_REGULAR), fg=LIGHT_GRAY, bg=BLACK)
        placeholder.pack(pady=SPACING_32)


class SystemTab(AdminTabContent):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, "⚙️ System Settings", **kwargs)
        self._create_content()
    
    def _create_content(self):
        """Create system settings tab content"""
        content = tk.Frame(self, bg=BLACK)
        content.pack(fill=tk.BOTH, expand=True, padx=SPACING_32, pady=SPACING_16)
        
        placeholder = tk.Label(content, text="System settings interface coming soon...", 
                              font=("Segoe UI", BODY_REGULAR), fg=LIGHT_GRAY, bg=BLACK)
        placeholder.pack(pady=SPACING_32)