"""Track Reading Progress Dialog"""
import tkinter as tk
from tkinter import messagebox
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
        "secondary": "#7A3BA3",
        "success": "#10B981"
    }


class TrackProgressDialog:
    """Dialog to track book reading progress"""
    def __init__(self, parent, book, app):
        self.parent = parent
        self.book = book
        self.app = app

        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"Track Progress: {getattr(book, 'title', 'Book')}")
        self.dialog.geometry("500x320")
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
            text="Update Reading Progress",
            font=("Segoe UI", 16, "bold"),
            bg=COLORS["background"],
            fg=COLORS["primary"]
        ).pack(pady=(18, 8), padx=20)

        tk.Label(
            self.dialog,
            text=getattr(self.book, "title", "Untitled"),
            font=("Segoe UI", 12),
            bg=COLORS["background"],
            fg="#666666"
        ).pack(pady=(0, 12), padx=20)

        # Current page entry
        frame = tk.Frame(self.dialog, bg=COLORS["background"])
        frame.pack(fill=tk.X, padx=20, pady=6)

        tk.Label(frame, text="Current Page:", font=("Segoe UI", 11), bg=COLORS["background"], fg=COLORS["text"]).pack(side=tk.LEFT)
        self.page_entry = tk.Entry(frame, font=("Segoe UI", 11), width=10)
        self.page_entry.pack(side=tk.LEFT, padx=(8, 0))
        self.page_entry.insert(0, str(getattr(self.book, "current_page", 0)))

        total_pages = getattr(self.book, "total_pages", 0) or 0
        tk.Label(frame, text=f"/ {total_pages}", font=("Segoe UI", 11), bg=COLORS["background"], fg="#666666").pack(side=tk.LEFT, padx=(6, 0))

        # Progress visual
        progress_frame = tk.Frame(self.dialog, bg=COLORS["background"])
        progress_frame.pack(fill=tk.X, padx=20, pady=12)

        progress_container = tk.Frame(progress_frame, bg="white", relief="solid", borderwidth=1, height=20)
        progress_container.pack(fill=tk.X)
        progress_container.pack_propagate(False)

        try:
            curr = int(getattr(self.book, "current_page", 0) or 0)
        except Exception:
            curr = 0
        try:
            total = int(total_pages)
        except Exception:
            total = 0

        if total > 0:
            progress_pct = max(0, min(100, int((curr / total) * 100)))
        else:
            progress_pct = 0

        progress_bar = tk.Frame(progress_container, bg=COLORS["primary"], height=20)
        progress_bar.place(x=0, y=0, relwidth=progress_pct / 100.0, relheight=1)

        tk.Label(progress_frame, text=f"{progress_pct}%", font=("Segoe UI", 10), bg=COLORS["background"], fg=COLORS["text"]).pack(anchor="e", pady=(6, 0), padx=4)

        # Buttons
        btn_frame = tk.Frame(self.dialog, bg=COLORS["background"])
        btn_frame.pack(fill=tk.X, padx=20, pady=(18, 12))

        save_btn = tk.Button(btn_frame, text="Save Progress", font=("Segoe UI", 11, "bold"),
                             bg=COLORS["success"], fg="white", relief="flat", padx=14, pady=8,
                             cursor="hand2", command=self.save_progress)
        save_btn.pack(side=tk.LEFT)

        cancel_btn = tk.Button(btn_frame, text="Cancel", font=("Segoe UI", 11),
                               bg="#cccccc", fg="#333333", relief="flat", padx=14, pady=8,
                               cursor="hand2", command=self.dialog.destroy)
        cancel_btn.pack(side=tk.LEFT, padx=(10, 0))

    def save_progress(self):
        """Validate and save progress to book and service"""
        try:
            val = self.page_entry.get().strip()
            if not val:
                messagebox.showerror("Error", "Please enter the current page number.")
                return
            try:
                page = int(val)
            except ValueError:
                messagebox.showerror("Error", "Page must be an integer.")
                return

            total = int(getattr(self.book, "total_pages", 0) or 0)
            if total > 0 and (page < 0 or page > total):
                messagebox.showerror("Error", f"Page must be between 0 and {total}.")
                return
            if page < 0:
                messagebox.showerror("Error", "Page cannot be negative.")
                return

            # update book object defensively
            try:
                setattr(self.book, "current_page", page)
            except Exception:
                pass

            if total > 0:
                prog = int((page / total) * 100)
                prog = max(0, min(100, prog))
                try:
                    setattr(self.book, "progress", prog)
                except Exception:
                    pass

            # Persist via service if available
            svc = getattr(self.app, "book_service", None)
            if svc:
                fn = getattr(svc, "update_book", None) or getattr(svc, "save_book", None) or getattr(svc, "add_book", None)
                if callable(fn):
                    try:
                        fn(self.book)
                    except Exception as e:
                        # non-fatal, but inform user
                        messagebox.showwarning("Warning", f"Saved locally but failed to persist to service: {e}")

            messagebox.showinfo("Success", "Progress updated.")
            self.dialog.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Error saving progress: {e}")