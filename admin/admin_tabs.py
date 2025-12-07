"""Admin Dashboard Tab Navigation System"""
import tkinter as tk
from tkinter import font
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

try:
    from styles.admin_theme import (
        DARK_GRAY, MEDIUM_GRAY, PRIMARY_PURPLE, WHITE, LIGHT_GRAY,
        SPACING_32, SPACING_16, SPACING_12, SPACING_8, BODY_REGULAR
    )
except ImportError:
    DARK_GRAY = "#1A1A1A"
    MEDIUM_GRAY = "#333333"
    PRIMARY_PURPLE = "#4B0082"
    WHITE = "#FFFFFF"
    LIGHT_GRAY = "#BFBFBF"
    SPACING_32 = 32
    SPACING_16 = 16
    SPACING_12 = 12
    SPACING_8 = 8
    BODY_REGULAR = 14


class AdminTabBar(tk.Frame):
    def __init__(self, parent, tabs, on_tab_change=None, **kwargs):
        super().__init__(parent, bg=DARK_GRAY, **kwargs)
        
        self.tabs = tabs
        self.on_tab_change = on_tab_change
        self.active_tab = 0
        self.tab_buttons = []
        
        self._create_tab_bar()
    
    def _create_tab_bar(self):
        """Create tab navigation bar"""
        # Border top
        border_top = tk.Frame(self, bg=MEDIUM_GRAY, height=1)
        border_top.pack(fill=tk.X)
        
        # Container frame
        container = tk.Frame(self, bg=DARK_GRAY)
        container.pack(fill=tk.X, padx=SPACING_32, pady=SPACING_16)
        
        # Tabs
        for idx, tab_name in enumerate(self.tabs):
            try:
                is_active = idx == self.active_tab
                btn = tk.Button(
                    container,
                    text=tab_name,
                    bg=PRIMARY_PURPLE if is_active else DARK_GRAY,
                    fg=WHITE if is_active else LIGHT_GRAY,
                    padx=SPACING_16,
                    pady=SPACING_12,
                    relief=tk.FLAT,
                    cursor="hand2",
                    font=("Segoe UI", BODY_REGULAR),
                    command=lambda i=idx: self._switch_tab(i)
                )
                btn.pack(side=tk.LEFT, padx=SPACING_8)
                self.tab_buttons.append(btn)
            except Exception as e:
                print(f"Error creating tab button {idx}: {e}")
        
        border_bottom = tk.Frame(self, bg=MEDIUM_GRAY, height=1)
        border_bottom.pack(fill=tk.X)
    
    def _switch_tab(self, tab_index):
        """Switch active tab"""
        self.active_tab = tab_index
        
        # Update button styles
        for idx, btn in enumerate(self.tab_buttons):
            if idx == tab_index:
                btn.config(bg=PRIMARY_PURPLE, fg=WHITE)
            else:
                btn.config(bg=DARK_GRAY, fg=LIGHT_GRAY)
        
        # Trigger callback
        if self.on_tab_change:
            self.on_tab_change(tab_index)