"""Search Results Dialog"""
import tkinter as tk
from tkinter import ttk
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

try:
    from config import COLORS
except ImportError:
    COLORS = {
        "background": "#f5f5f5",
        "text": "#333333",
        "primary": "#4B0082"
    }


class SearchResultsDialog:
    """Dialog to display search results"""
    def __init__(self, parent, results, app):
        self.parent = parent
        self.results = results
        self.app = app

        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"Search Results ({len(results)} found)")
        self.dialog.geometry("800x600")
        self.dialog.configure(bg=COLORS["background"])
        self.dialog.transient(parent)
        self.dialog.grab_set()

        self.create_widgets()
        self.center_dialog()

    def center_dialog(self):
        """Center dialog on screen"""
        try:
            self.dialog.update_idletasks()
            width = self.dialog.winfo_width()
            height = self.dialog.winfo_height()
            x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
            y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
            self.dialog.geometry(f'{width}x{height}+{x}+{y}')
        except Exception as e:
            print(f"Error centering dialog: {e}")

    def create_widgets(self):
        """Create dialog widgets"""
        # Title
        tk.Label(
            self.dialog,
            text=f"Search Results - {len(self.results)} books found",
            font=("Segoe UI", 14, "bold"),
            bg=COLORS["background"],
            fg=COLORS["primary"]
        ).pack(pady=(15, 10), padx=20)

        # Results list
        if self.results:
            # Create treeview
            tree_frame = tk.Frame(self.dialog, bg=COLORS["background"])
            tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

            columns = ("Title", "Author", "Genre", "Status")
            tree = ttk.Treeview(tree_frame, columns=columns, height=15)
            
            # Define column headings
            tree.column("#0", width=0, stretch=tk.NO)
            tree.column("Title", anchor=tk.W, width=300)
            tree.column("Author", anchor=tk.W, width=150)
            tree.column("Genre", anchor=tk.W, width=150)
            tree.column("Status", anchor=tk.W, width=100)

            tree.heading("#0", text="", anchor=tk.W)
            tree.heading("Title", text="Title", anchor=tk.W)
            tree.heading("Author", text="Author", anchor=tk.W)
            tree.heading("Genre", text="Genre", anchor=tk.W)
            tree.heading("Status", text="Status", anchor=tk.W)

            # Add results to tree
            for idx, book in enumerate(self.results):
                title = getattr(book, "title", "")
                author = getattr(book, "author", "")
                genre = getattr(book, "genre", "")
                status = getattr(book, "status", "")
                tree.insert(parent="", index="end", iid=f"item{idx}", text="",
                           values=(title, author, genre, status))

            # Scrollbar
            scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
            # ttk.Treeview expects 'yscrollcommand' to be set to the scrollbar.set callable
            tree.configure(yscrollcommand=scrollbar.set)

            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        else:
            tk.Label(
                self.dialog,
                text="No results found",
                font=("Segoe UI", 12),
                bg=COLORS["background"],
                fg="#999999"
            ).pack(pady=50)

        # Close button
        close_btn = tk.Button(
            self.dialog,
            text="Close",
            font=("Segoe UI", 11),
            bg=COLORS["primary"],
            fg="white",
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.dialog.destroy
        )
        close_btn.pack(pady=(0, 15))