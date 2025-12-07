# components/header.py
import tkinter as tk
from config import COLORS


class Header:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app

        # Create header frame
        self.frame = tk.Frame(
            parent,
            bg=COLORS["primary"],
            height=60
        )
        self.frame.pack(fill=tk.X)
        self.frame.pack_propagate(False)

        self.create_logo()
        self.create_navigation()

    def create_logo(self):
        """Create logo section"""
        logo_frame = tk.Frame(self.frame, bg=COLORS["primary"])
        logo_frame.pack(side=tk.LEFT, padx=20)

        # Logo text
        tk.Label(
            logo_frame,
            text="📚",
            font=("Segoe UI", 24),
            bg=COLORS["primary"],
            fg="white"
        ).pack(side=tk.LEFT, padx=(0, 10))

        tk.Label(
            logo_frame,
            text="Libris Core",
            font=("Segoe UI", 20, "bold"),
            fg="white",
            bg=COLORS["primary"]
        ).pack(side=tk.LEFT)

        tk.Label(
            logo_frame,
            text="Library Management System",
            font=("Segoe UI", 12),
            fg=COLORS["light"],
            bg=COLORS["primary"]
        ).pack(side=tk.LEFT, padx=(10, 0))

    def create_navigation(self):
        """Create navigation buttons"""
        nav_frame = tk.Frame(self.frame, bg=COLORS["primary"])
        nav_frame.pack(side=tk.RIGHT, padx=20)

        nav_items = [
            ("📚 Library", self.app.show_library),
            ("📊 Stats", self.app.show_stats),
            ("🏷️ Categories", self.app.show_categories),
            ("➕ Add Book", self.app.show_add_book),
            ("🔍 Search", self.app.show_search)
        ]

        for text, command in nav_items:
            btn = tk.Button(
                nav_frame,
                text=text,
                font=("Segoe UI", 10),
                bg=COLORS["secondary"],
                fg="white",
                activebackground=COLORS["accent"],
                activeforeground="white",
                relief="flat",
                padx=15,
                pady=5,
                cursor="hand2",
                command=command
            )
            btn.pack(side=tk.LEFT, padx=5)

    def refresh(self):
        """Refresh header display"""
        pass