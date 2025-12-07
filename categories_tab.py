# components/categories_tab.py
import tkinter as tk
from tkinter import ttk
from config import COLORS
from components.dialogs.category_editor import CategoryEditorDialog


class CategoriesTab:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.frame = tk.Frame(parent, bg=COLORS["background"])

        self.create_widgets()
        self.refresh()

    def create_widgets(self):
        """Create all widgets for categories tab"""
        # Title and add button
        title_frame = tk.Frame(self.frame, bg=COLORS["background"])
        title_frame.pack(fill=tk.X, padx=20, pady=(20, 10))

        tk.Label(
            title_frame,
            text="🏷️ Custom Categories",
            font=("Segoe UI", 24, "bold"),
            bg=COLORS["background"],
            fg=COLORS["primary"]
        ).pack(side=tk.LEFT)

        # Add category button
        add_button = tk.Button(
            title_frame,
            text="➕ Create New Category",
            font=("Segoe UI", 10, "bold"),
            bg=COLORS["success"],
            fg="white",
            activebackground=COLORS["success"],
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.create_category
        )
        add_button.pack(side=tk.RIGHT)

        # Categories display area
        self.create_categories_display()

    def create_categories_display(self):
        """Create scrollable area for categories"""
        # Create container
        container = tk.Frame(self.frame, bg=COLORS["background"])
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Create canvas for scrolling
        self.canvas = tk.Canvas(
            container,
            bg=COLORS["background"],
            highlightthickness=0
        )
        scrollbar = ttk.Scrollbar(
            container,
            orient="vertical",
            command=self.canvas.yview
        )

        # Create scrollable frame
        self.scrollable_frame = tk.Frame(self.canvas, bg=COLORS["background"])
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind mouse wheel
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def create_category(self):
        """Open dialog to create new category"""
        dialog = CategoryEditorDialog(
            self.app.root,
            self.app
        )

        # use getattr to avoid attribute-access error if dialog lacks `result`
        if getattr(dialog, "result", False):
            self.refresh()

    def edit_category(self, category):
        """Open dialog to edit category"""
        dialog = CategoryEditorDialog(
            self.app.root,
            self.app,
            category=category
        )

        # use getattr to avoid attribute-access error if dialog lacks `result`
        if getattr(dialog, "result", False):
            self.refresh()

    def delete_category(self, category):
        """Delete a category"""
        from tkinter import messagebox

        response = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete the category '{category.name}'?\n"
            f"This will remove it from {category.book_count} book(s)."
        )

        if response:
            success = self.app.category_service.delete_category(category.name)
            if success:
                # Update books that had this category
                books = self.app.book_service.get_all_books()
                for book in books:
                    if category.name in book.categories:
                        book.categories.remove(category.name)
                        if not book.categories:
                            book.categories.append("General")

                # Refresh display
                self.refresh()
                messagebox.showinfo(
                    "Success",
                    f"Category '{category.name}' deleted successfully!"
                )

    def display_categories(self):
        """Display all categories"""
        # Clear existing categories
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Get categories from service
        categories = self.app.category_service.get_all_categories()

        if not categories:
            self.show_empty_state()
            return

        # Update book counts
        self.app.category_service.update_book_counts(self.app.book_service)

        # Display categories in grid (3 columns)
        for i, category in enumerate(categories):
            row = i // 3
            col = i % 3

            # Create category card
            category_card = self.create_category_card(category)
            category_card.grid(
                row=row,
                column=col,
                padx=10,
                pady=10,
                sticky="nsew"
            )

            # Configure grid weights
            self.scrollable_frame.grid_columnconfigure(col, weight=1)
            self.scrollable_frame.grid_rowconfigure(row, weight=1)

    def create_category_card(self, category):
        """Create a category card widget"""
        card = tk.Frame(
            self.scrollable_frame,
            bg="white",
            relief="solid",
            borderwidth=1,
            width=300,
            height=120
        )
        card.grid_propagate(False)

        # Color indicator
        color_indicator = tk.Frame(
            card,
            bg=category.color,
            width=10,
            height=120
        )
        color_indicator.pack(side=tk.LEFT)

        # Category info
        info_frame = tk.Frame(card, bg="white")
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15)

        # Category name
        tk.Label(
            info_frame,
            text=category.name,
            font=("Segoe UI", 14, "bold"),
            bg="white",
            fg=COLORS["text"]
        ).pack(anchor="w", pady=(15, 5))

        # Book count
        tk.Label(
            info_frame,
            text=f"{category.book_count} books",
            font=("Segoe UI", 10),
            bg="white",
            fg="#666666"
        ).pack(anchor="w")

        # Actions frame
        actions_frame = tk.Frame(info_frame, bg="white")
        actions_frame.pack(anchor="w", pady=(10, 0))

        # Edit button
        edit_button = tk.Button(
            actions_frame,
            text="✏️ Edit",
            font=("Segoe UI", 9),
            bg="white",
            fg=COLORS["primary"],
            activebackground="white",
            activeforeground=COLORS["secondary"],
            relief="flat",
            cursor="hand2",
            command=lambda c=category: self.edit_category(c)
        )
        edit_button.pack(side=tk.LEFT, padx=(0, 10))

        # Delete button
        delete_button = tk.Button(
            actions_frame,
            text="🗑️ Delete",
            font=("Segoe UI", 9),
            bg="white",
            fg=COLORS["danger"],
            activebackground="white",
            activeforeground=COLORS["danger"],
            relief="flat",
            cursor="hand2",
            command=lambda c=category: self.delete_category(c)
        )
        delete_button.pack(side=tk.LEFT)

        return card

    def show_empty_state(self):
        empty_frame.pack(fill=tk.BOTH, expand=True, pady=100)
        empty_frame = tk.Frame(self.scrollable_frame, bg=COLORS["background"])
        tk.Label(me.pack(fill=tk.BOTH, expand=True, pady=100)
            empty_frame,
            text="🏷️",
            font=("Segoe UI", 72),
            bg=COLORS["background"],
            fg=COLORS["light"]72),
        ).pack()OLORS["background"],
            fg=COLORS["light"]
        tk.Label(
            empty_frame,
            text="No categories yet",
            font=("Segoe UI", 16),
            bg=COLORS["background"],,
            fg=COLORS["text"] 16),
        ).pack(pady=10)background"],
            fg=COLORS["text"]
        tk.Label(dy=10)
            empty_frame,
            text="Create your first category to organize books!",
            font=("Segoe UI", 12),
            bg=COLORS["background"],category to organize books!",
            fg=COLORS["text"] 12),
        ).pack()OLORS["background"],
            fg=COLORS["text"]
        create_button = tk.Button(
            empty_frame,
            text="➕ Create Category",
            font=("Segoe UI", 11, "bold"),
            bg=COLORS["primary"],ry",
            fg="white",e UI", 11, "bold"),
            activebackground=COLORS["secondary"],
            activeforeground="white",
            relief="flat",nd=COLORS["secondary"],
            padx=20,reground="white",
            pady=10,flat",
            cursor="hand2",
            command=self.create_category
        )   cursor="hand2",
        create_button.pack(pady=20)egory
        )
    def refresh(self):pack(pady=20)
        """Refresh categories display"""
        self.display_categories()
        """Refresh categories display"""
    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        """Handle mouse wheel scrolling"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")