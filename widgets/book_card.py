# components/widgets/book_card.py
import tkinter as tk
from config import COLORS, STATUS_COLORS


class BookCard:
    def __init__(self, parent, book, app):
        self.parent = parent
        self.book = book
        self.app = app

        # Create book card frame
        self.frame = tk.Frame(
            parent,
            bg="white",
            relief="solid",
            borderwidth=1,
            width=250,
            height=350
        )
        self.frame.grid_propagate(False)

        # Simple book card content
        cover_frame = tk.Frame(
            self.frame,
            bg="#f0f0f0",
            width=200,
            height=200
        )
        cover_frame.place(x=25, y=20)
        cover_frame.pack_propagate(False)

        # Book icon
        tk.Label(
            cover_frame,
            text="📚",
            font=("Segoe UI", 48),
            bg="#f0f0f0"
        ).pack(expand=True)

        # Title
        title = book.title[:25] + "..." if len(book.title) > 25 else book.title
        tk.Label(
            self.frame,
            text=title,
            font=("Segoe UI", 11, "bold"),
            bg="white",
            fg=COLORS["text"],
            wraplength=220
        ).place(x=15, y=240)

        # Author
        author = f"by {book.author[:20]}..." if len(book.author) > 20 else f"by {book.author}"
        tk.Label(
            self.frame,
            text=author,
            font=("Segoe UI", 9),
            bg="white",
            fg="#666666"
        ).place(x=15, y=265)

        # Status
        tk.Label(
            self.frame,
            text=book.status,
            font=("Segoe UI", 9, "bold"),
            bg=STATUS_COLORS.get(book.status, COLORS["light"]),
            fg="white",
            padx=10,
            pady=2
        ).place(x=15, y=290)

        # View button
        tk.Button(
            self.frame,
            text="View",
            font=("Segoe UI", 9),
            bg=COLORS["primary"],
            fg="white",
            relief="flat",
            padx=15,
            pady=2,
            command=lambda: print(f"Viewing {book.title}")
        ).place(x=80, y=320)