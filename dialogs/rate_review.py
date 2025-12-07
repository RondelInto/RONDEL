"""Rate and Review Dialog"""
import tkinter as tk
from tkinter import scrolledtext, messagebox
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
        "primary": "#4B0082",
        "warning": "#F59E0B",
        "success": "#10B981"
    }


class RateReviewDialog:
    """Dialog to rate and review a book"""
    def __init__(self, parent, book, app):
        self.parent = parent
        self.book = book
        self.app = app
        self.rating = getattr(book, "rating", 0) or 0

        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"Rate & Review: {getattr(book, 'title', 'Book')}")
        self.dialog.geometry("600x500")
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
        tk.Label(
            self.dialog,
            text="Rate & Review",
            font=("Segoe UI", 16, "bold"),
            bg=COLORS["background"],
            fg=COLORS["primary"]
        ).pack(pady=(20, 10), padx=20)

        tk.Label(
            self.dialog,
            text=getattr(self.book, "title", ""),
            font=("Segoe UI", 12),
            bg=COLORS["background"],
            fg="#666666"
        ).pack(pady=(0, 20), padx=20)

        rating_frame = tk.Frame(self.dialog, bg=COLORS["background"])
        rating_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(
            rating_frame,
            text="Rating:",
            font=("Segoe UI", 11, "bold"),
            bg=COLORS["background"],
            fg=COLORS["text"]
        ).pack(anchor="w")

        stars_frame = tk.Frame(rating_frame, bg=COLORS["background"])
        stars_frame.pack(anchor="w", pady=(10, 0))

        self.star_buttons = []
        for i in range(1, 6):
            btn = tk.Button(
                stars_frame,
                text="★",
                font=("Segoe UI", 24),
                bg=COLORS["background"],
                fg=COLORS["warning"] if i <= self.rating else "#cccccc",
                relief="flat",
                cursor="hand2",
                command=lambda star=i: self.set_rating(star)
            )
            btn.pack(side=tk.LEFT, padx=2)
            self.star_buttons.append(btn)

        self.rating_label = tk.Label(
            rating_frame,
            text=f"{self.rating:.1f}/5.0",
            font=("Segoe UI", 12),
            bg=COLORS["background"],
            fg=COLORS["text"]
        )
        self.rating_label.pack(side=tk.LEFT, pady=(10, 0), padx=(10, 0))

        review_frame = tk.Frame(self.dialog, bg=COLORS["background"])
        review_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        tk.Label(
            review_frame,
            text="Review (Optional):",
            font=("Segoe UI", 11, "bold"),
            bg=COLORS["background"],
            fg=COLORS["text"]
        ).pack(anchor="w", pady=(0, 10))

        self.review_text = scrolledtext.ScrolledText(
            review_frame,
            font=("Segoe UI", 10),
            height=8,
            bg="white",
            fg=COLORS["text"],
            relief="solid",
            borderwidth=1,
            wrap=tk.WORD
        )
        self.review_text.pack(fill=tk.BOTH, expand=True)
        self.review_text.insert("1.0", getattr(self.book, "review", "") or "")

        button_frame = tk.Frame(self.dialog, bg=COLORS["background"])
        button_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        save_btn = tk.Button(
            button_frame,
            text="Save Review",
            font=("Segoe UI", 11, "bold"),
            bg=COLORS["success"],
            fg="white",
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.save_review
        )
        save_btn.pack(side=tk.LEFT, padx=(0, 10))

        cancel_btn = tk.Button(
            button_frame,
            text="Cancel",
            font=("Segoe UI", 11),
            bg="#cccccc",
            fg="#333333",
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.dialog.destroy
        )
        cancel_btn.pack(side=tk.LEFT)

    def set_rating(self, stars):
        """Set rating by clicking stars"""
        self.rating = stars
        self.rating_label.config(text=f"{self.rating:.1f}/5.0")

        for i, btn in enumerate(self.star_buttons, 1):
            btn.config(fg=COLORS["warning"] if i <= stars else "#cccccc")

    def save_review(self):
        """Save review and rating"""
        try:
            review_text = self.review_text.get("1.0", tk.END).strip()

            # Update book defensively
            try:
                setattr(self.book, "rating", self.rating)
                setattr(self.book, "review", review_text)
            except Exception:
                pass

            # Save to service if available
            svc = getattr(self.app, "book_service", None)
            if svc:
                fn = getattr(svc, "update_book", None) or getattr(svc, "save_book", None) or getattr(svc, "add_book", None)
                if callable(fn):
                    fn(self.book)

            messagebox.showinfo("Success", "Review saved successfully!")
            self.dialog.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Error saving review: {e}")