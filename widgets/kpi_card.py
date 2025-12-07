# components/widgets/kpi_card.py
import tkinter as tk
from config import COLORS


class KPICard:
    def __init__(self, parent, title, value, icon, color):
        self.parent = parent
        self.title = title
        self.value = value
        self.icon = icon
        self.color = color
        
        # Create card frame
        self.frame = tk.Frame(
            parent,
            bg="white",
            relief="solid",
            borderwidth=1
        )
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create KPI card widgets"""
        # Icon
        tk.Label(
            self.frame,
            text=self.icon,
            font=("Segoe UI", 24),
            bg="white",
            fg=self.color
        ).pack(pady=(20, 5))
        
        # Value
        tk.Label(
            self.frame,
            text=str(self.value),
            font=("Segoe UI", 20, "bold"),
            bg="white",
            fg=COLORS["text"]
        ).pack()
        
        # Title
        tk.Label(
            self.frame,
            text=self.title,
            font=("Segoe UI", 10),
            bg="white",
            fg=COLORS["text"]
        ).pack(pady=(5, 20))
