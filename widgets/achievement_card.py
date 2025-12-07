# components/widgets/achievement_card.py
import tkinter as tk
from config import COLORS


class AchievementCard:
    def __init__(self, parent, achievement):
        self.parent = parent
        self.achievement = achievement
        
        # Create card frame
        self.frame = tk.Frame(
            parent,
            bg="white" if achievement.unlocked else "#f0f0f0",
            relief="solid",
            borderwidth=1,
            width=250,
            height=100
        )
        self.frame.grid_propagate(False)
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create achievement card widgets"""
        # Icon
        icon_label = tk.Label(
            self.frame,
            text=self.achievement.icon,
            font=("Segoe UI", 24),
            bg=self.frame["bg"],
            fg=COLORS["primary"] if self.achievement.unlocked else "#cccccc"
        )
        icon_label.place(x=20, y=30)
        
        # Name
        tk.Label(
            self.frame,
            text=self.achievement.name,
            font=("Segoe UI", 12, "bold"),
            bg=self.frame["bg"],
            fg=COLORS["text"] if self.achievement.unlocked else "#999999"
        ).place(x=70, y=25)
        
        # Description
        tk.Label(
            self.frame,
            text=self.achievement.description,
            font=("Segoe UI", 9),
            bg=self.frame["bg"],
            fg=COLORS["text"] if self.achievement.unlocked else "#999999",
            wraplength=150
        ).place(x=70, y=50)
        
        # Lock/Unlock indicator
        if not self.achievement.unlocked:
            tk.Label(
                self.frame,
                text="🔒 Locked",
                font=("Segoe UI", 8),
                bg=self.frame["bg"],
                fg="#999999"
            ).place(x=180, y=10)
