"""Category Editor Dialog"""
import tkinter as tk
from tkinter import messagebox, colorchooser
import sys
import os
from types import SimpleNamespace

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

try:
    from config import COLORS
    from models import Category
except ImportError:
    COLORS = {
        "background": "#f5f5f5",
        "text": "#333333",
        "primary": "#4B0082",
        "success": "#10B981"
    }
    Category = None


class CategoryEditorDialog:
    """Dialog to edit categories"""
    def __init__(self, parent, category=None, app=None):
        self.parent = parent
        self.category = category
        self.app = app
        # use getattr to avoid AttributeError if category provided but missing color
        self.selected_color = getattr(category, "color", "#4B0082") if category is not None else "#4B0082"

        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Edit Category" if category else "New Category")
        self.dialog.geometry("400x300")
        self.dialog.configure(bg=COLORS["background"])
        self.dialog.transient(parent)
        self.dialog.grab_set()
        # improve UX: fixed size and focus
        self.dialog.resizable(False, False)

        self.create_widgets()
        # focus the name entry for faster input
        try:
            self.name_entry.focus_set()
        except Exception:
            pass
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
            text="Category Details",
            font=("Segoe UI", 16, "bold"),
            bg=COLORS["background"],
            fg=COLORS["primary"]
        ).pack(pady=(20, 20), padx=20)

        # Name section
        name_frame = tk.Frame(self.dialog, bg=COLORS["background"])
        name_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(
            name_frame,
            text="Name:",
            font=("Segoe UI", 11),
            bg=COLORS["background"],
            fg=COLORS["text"]
        ).pack(side=tk.LEFT, anchor="w")

        self.name_entry = tk.Entry(name_frame, font=("Segoe UI", 11), width=30)
        self.name_entry.pack(side=tk.LEFT, padx=(10, 0))
        if self.category:
            self.name_entry.insert(0, getattr(self.category, "name", ""))

        # Color section
        color_frame = tk.Frame(self.dialog, bg=COLORS["background"])
        color_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(
            color_frame,
            text="Color:",
            font=("Segoe UI", 11),
            bg=COLORS["background"],
            fg=COLORS["text"]
        ).pack(side=tk.LEFT, anchor="w")

        self.color_display = tk.Label(
            color_frame,
            text="   ",
            bg=self.selected_color,
            relief="solid",
            borderwidth=1,
            width=5
        )
        self.color_display.pack(side=tk.LEFT, padx=(10, 5))

        color_btn = tk.Button(
            color_frame,
            text="Choose Color",
            font=("Segoe UI", 10),
            bg=COLORS["primary"],
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.choose_color
        )
        color_btn.pack(side=tk.LEFT)

        # Buttons
        button_frame = tk.Frame(self.dialog, bg=COLORS["background"])
        button_frame.pack(fill=tk.X, padx=20, pady=(30, 20))

        save_btn = tk.Button(
            button_frame,
            text="Save",
            font=("Segoe UI", 11, "bold"),
            bg=COLORS["success"],
            fg="white",
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.save_category
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

    def choose_color(self):
        """Open color chooser"""
        color = colorchooser.askcolor(color=self.selected_color, title="Choose Category Color")
        if color[1]:  # If user didn't cancel
            self.selected_color = color[1]
            self.color_display.config(bg=self.selected_color)

    def save_category(self):
        """Save category changes"""
        try:
            name = self.name_entry.get().strip()

            if not name:
                messagebox.showerror("Error", "Category name cannot be empty")
                return

            if self.category:
                # defensive setattr
                setattr(self.category, "name", name)
                setattr(self.category, "color", self.selected_color)
            else:
                # create new Category instance if available, otherwise a simple fallback object
                if Category is not None:
                    try:
                        self.category = Category(name=name, color=self.selected_color)
                    except TypeError:
                        # fallback if constructor signature differs: use a simple namespace object
                        self.category = SimpleNamespace(name=name, color=self.selected_color)
                else:
                    class _CategoryFallback:
                        pass
                    self.category = _CategoryFallback()
                    setattr(self.category, "name", name)
                    setattr(self.category, "color", self.selected_color)

            # Save to service if available (defensive)
            svc = getattr(self.app, "category_service", None)
            if svc:
                save_fn = getattr(svc, "save_category", None) or getattr(svc, "add_category", None) or getattr(svc, "update_category", None)
                if callable(save_fn):
                    save_fn(self.category)

            messagebox.showinfo("Success", "Category saved successfully!")
            self.dialog.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Error saving category: {e}")