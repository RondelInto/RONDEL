"""Admin Dashboard Header Component"""
import tkinter as tk
from tkinter import font
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

try:
    from styles.admin_theme import (
        DARK_GRAY, PRIMARY_PURPLE, WHITE, LIGHT_GRAY, MEDIUM_GRAY,
        SPACING_16, SPACING_12, BODY_LARGE, BODY_REGULAR, HEADER_HEIGHT
    )
except ImportError:
    DARK_GRAY = "#1A1A1A"
    PRIMARY_PURPLE = "#4B0082"
    WHITE = "#FFFFFF"
    LIGHT_GRAY = "#BFBFBF"
    MEDIUM_GRAY = "#333333"
    SPACING_16 = 16
    SPACING_12 = 12
    BODY_LARGE = 16
    BODY_REGULAR = 14
    HEADER_HEIGHT = 72


class AdminHeader(tk.Frame):
    def __init__(self, parent, admin_system, **kwargs):
        super().__init__(parent, bg=DARK_GRAY, height=HEADER_HEIGHT, **kwargs)
        
        self.parent = parent
        self.admin_system = admin_system
        self.pack_propagate(False)
        
        # Create header content
        self._create_header_content()
    
    def _create_header_content(self):
        """Create header layout with logo and logout button"""
        
        # Left section container
        left_section = tk.Frame(self, bg=DARK_GRAY)
        left_section.pack(side=tk.LEFT, padx=SPACING_16, pady=SPACING_16, fill=tk.BOTH, expand=True)
        
        # Logo placeholder (48x48)
        logo_frame = tk.Frame(left_section, bg=PRIMARY_PURPLE, width=48, height=48)
        logo_frame.pack(side=tk.LEFT, padx=(0, SPACING_12))
        logo_frame.pack_propagate(False)
        
        # Use tkinter.font.Font objects (fixes Pylance type errors)
        logo_font = font.Font(family="Segoe UI", size=24, weight="bold")
        logo_text = tk.Label(logo_frame, text="LC", font=logo_font, 
                            fg=WHITE, bg=PRIMARY_PURPLE)
        logo_text.pack(expand=True)
        
        # Text stack
        text_stack = tk.Frame(left_section, bg=DARK_GRAY)
        text_stack.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        title_font = font.Font(family="Segoe UI", size=BODY_LARGE, weight="bold")
        title = tk.Label(text_stack, text="Libris Core Admin", font=title_font, 
                        fg=WHITE, bg=DARK_GRAY)
        title.pack(anchor="w")
        
        # Get current user from admin_system
        current_user = getattr(self.admin_system, 'current_user', 'Administrator')
        
        subtitle_font = font.Font(family="Segoe UI", size=BODY_REGULAR)
        subtitle = tk.Label(text_stack, text=f"Logged in as {current_user}", 
                           font=subtitle_font, fg=LIGHT_GRAY, bg=DARK_GRAY)
        subtitle.pack(anchor="w")
        
        # Right section - Logout button
        right_section = tk.Frame(self, bg=DARK_GRAY)
        right_section.pack(side=tk.RIGHT, padx=SPACING_16, pady=SPACING_16)
        
        logout_btn = tk.Button(right_section, text="🚪 Logout", bg=PRIMARY_PURPLE, 
                              fg=WHITE, padx=20, pady=10, relief=tk.FLAT,
                              cursor="hand2", command=self._logout)
        logout_btn.pack()
        
        # Border bottom
        border = tk.Frame(self, bg=MEDIUM_GRAY, height=1)
        border.pack(side=tk.BOTTOM, fill=tk.X)
    
    def _logout(self):
        """Handle logout action"""
        if hasattr(self.admin_system, '_logout'):
            self.admin_system._logout()
        else:
            print("Logout method not found in admin_system")