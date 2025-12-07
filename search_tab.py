# components/search_tab.py
import tkinter as tk
from tkinter import ttk, messagebox
from config import COLORS, STATUS_COLORS
from components.dialogs.book_details import BookDetailsDialog
from utils.helpers import get_star_rating, truncate_text


class SearchTab:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.frame = tk.Frame(parent, bg=COLORS["background"])

        # Search variables
        self.search_query = tk.StringVar(value="")
        self.status_filter = tk.StringVar(value="All")
        self.category_filter = tk.StringVar(value="All")
        self.rating_filter = tk.StringVar(value="0")

        self.create_widgets()

    def create_widgets(self):
        """Create all widgets for search tab"""
        # Create main container
        main_container = tk.Frame(self.frame, bg=COLORS["background"])
        main_container.pack(fill=tk.BOTH, expand=True)

        # Create search controls
        self.create_search_controls(main_container)

        # Create filters
        self.create_filters(main_container)

        # Create results display
        self.create_results_display(main_container)

    def create_search_controls(self, parent):
        """Create search bar and controls"""
        search_frame = tk.Frame(parent, bg=COLORS["background"])
        search_frame.pack(fill=tk.X, padx=20, pady=20)

        # Title
        tk.Label(
            search_frame,
            text="🔍 Search Your Library",
            font=("Segoe UI", 18, "bold"),
            bg=COLORS["background"],
            fg=COLORS["primary"]
        ).pack(anchor="w", pady=(0, 15))

        # Search bar
        search_bar_frame = tk.Frame(search_frame, bg=COLORS["background"])
        search_bar_frame.pack(fill=tk.X)

        tk.Label(
            search_bar_frame,
            text="Search:",
            font=("Segoe UI", 11),
            bg=COLORS["background"],
            fg=COLORS["text"]
        ).pack(side=tk.LEFT, padx=(0, 10))

        search_entry = tk.Entry(
            search_bar_frame,
            textvariable=self.search_query,
            font=("Segoe UI", 12),
            width=40
        )
        search_entry.pack(side=tk.LEFT, padx=(0, 10))
        search_entry.bind("<KeyRelease>", lambda e: self.perform_search())

        # Clear button
        clear_button = tk.Button(
            search_bar_frame,
            text="Clear",
            font=("Segoe UI", 10),
            bg=COLORS["light"],
            fg=COLORS["text"],
            activebackground=COLORS["accent"],
            activeforeground=COLORS["text"],
            relief="flat",
            padx=15,
            pady=5,
            cursor="hand2",
            command=self.clear_search
        )
        clear_button.pack(side=tk.LEFT)

    def create_filters(self, parent):
        """Create search filters"""
        filters_frame = tk.Frame(parent, bg=COLORS["background"])
        filters_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        tk.Label(
            filters_frame,
            text="Filters:",
            font=("Segoe UI", 11, "bold"),
            bg=COLORS["background"],
            fg=COLORS["text"]
        ).pack(anchor="w", pady=(0, 10))

        # Create filter options in a grid
        filter_grid = tk.Frame(filters_frame, bg=COLORS["background"])
        filter_grid.pack(fill=tk.X)

        # Status filter
        status_frame = tk.Frame(filter_grid, bg=COLORS["background"])
        status_frame.grid(row=0, column=0, padx=(0, 40), pady=5, sticky="w")

        tk.Label(
            status_frame,
            text="Status:",
            font=("Segoe UI", 10),
            bg=COLORS["background"],
            fg=COLORS["text"]
        ).pack(anchor="w")

        statuses = ["All", "Reading", "Completed", "On Hold", "Not Started"]
        for status in statuses:
            tk.Radiobutton(
                status_frame,
                text=status,
                variable=self.status_filter,
                value=status,
                bg=COLORS["background"],
                fg=COLORS["text"],
                command=self.perform_search
            ).pack(anchor="w")

        # Category filter
        category_frame = tk.Frame(filter_grid, bg=COLORS["background"])
        category_frame.grid(row=0, column=1, padx=(0, 40), pady=5, sticky="w")

        tk.Label(
            category_frame,
            text="Category:",
            font=("Segoe UI", 10),
            bg=COLORS["background"],
            fg=COLORS["text"]
        ).pack(anchor="w")

        # Get categories (defensive)
        try:
            cats = []
            if getattr(self.app, 'category_service', None) and hasattr(self.app.category_service, 'get_all_categories'):
                cats = self.app.category_service.get_all_categories() or []
            else:
                try:
                    import services as services_pkg
                    if getattr(services_pkg, 'category_service', None):
                        cats = services_pkg.category_service.get_all_categories() or []
                except Exception:
                    cats = []
            categories = ["All"] + [getattr(c, 'name', str(c)) for c in cats]
        except Exception:
            categories = ["All"]
        category_menu = ttk.Combobox(
            category_frame,
            textvariable=self.category_filter,
            values=categories,
            state="readonly",
            width=15,
            font=("Segoe UI", 9)
        )
        category_menu.pack(anchor="w")
        category_menu.bind("<<ComboboxSelected>>", lambda e: self.perform_search())

        # Rating filter
        rating_frame = tk.Frame(filter_grid, bg=COLORS["background"])
        rating_frame.grid(row=0, column=2, pady=5, sticky="w")

        tk.Label(
            rating_frame,
            text="Min Rating:",
            font=("Segoe UI", 10),
            bg=COLORS["background"],
            fg=COLORS["text"]
        ).pack(anchor="w")

        rating_menu = ttk.Combobox(
            rating_frame,
            textvariable=self.rating_filter,
            values=["0", "1", "2", "3", "4", "5"],
            state="readonly",
            width=5,
            font=("Segoe UI", 9)
        )
        rating_menu.pack(anchor="w")
        rating_menu.bind("<<ComboboxSelected>>", lambda e: self.perform_search())

    def create_results_display(self, parent):
        """Create results display area"""
        # Results container
        results_container = tk.Frame(parent, bg=COLORS["background"])
        results_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        # Results count label
        self.results_count_label = tk.Label(
            results_container,
            text="Results: 0",
            font=("Segoe UI", 11, "bold"),
            bg=COLORS["background"],
            fg=COLORS["text"]
        )
        self.results_count_label.pack(anchor="w", pady=(0, 10))

        # Create scrollable results area
        self.canvas = tk.Canvas(
            results_container,
            bg=COLORS["background"],
            highlightthickness=0
        )
        scrollbar = ttk.Scrollbar(
            results_container,
            orient="vertical",
            command=self.canvas.yview
        )

        # Create scrollable frame
        self.results_frame = tk.Frame(self.canvas, bg=COLORS["background"])
        self.results_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.results_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind mouse wheel
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def perform_search(self, event=None):
        """Perform search with current filters"""
        query = self.search_query.get().strip()
        status = self.status_filter.get()
        category = self.category_filter.get()
        min_rating = float(self.rating_filter.get())

        # Build filters dictionary
        filters = {}
        if status != "All":
            filters['status'] = status
        if category != "All":
            filters['category'] = category
        if min_rating > 0:
            filters['min_rating'] = min_rating

        # Perform search
        results = self.app.book_service.search_books(query, filters)

        # Update results count
        self.results_count_label.config(text=f"Results: {len(results)}")

        # Display results
        self.display_results(results)

    def display_results(self, books):
        """Display search results"""
        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        if not books:
            self.show_empty_results()
            return

        # Display books in list view
        for i, book in enumerate(books):
            result_row = self.create_result_row(book, i)
            result_row.pack(fill=tk.X, pady=2)

    def create_result_row(self, book, index):
        """Create a search result row"""
        # Alternate row colors
        row_color = "white" if index % 2 == 0 else COLORS["light_bg"]

        row = tk.Frame(
            self.results_frame,
            bg=row_color,
            height=60
        )
        row.pack_propagate(False)

        # Book info (left side)
        info_frame = tk.Frame(row, bg=row_color)
        info_frame.pack(side=tk.LEFT, fill=tk.Y, expand=True, padx=20)

        # Title
        title_label = tk.Label(
            info_frame,
            text=truncate_text(book.title, 40),
            font=("Segoe UI", 11, "bold"),
            bg=row_color,
            fg=COLORS["text"],
            anchor="w"
        )
        title_label.pack(anchor="w", pady=(10, 0))

        # Author and details
        details_frame = tk.Frame(info_frame, bg=row_color)
        details_frame.pack(anchor="w", pady=(0, 10))

        tk.Label(
            details_frame,
            text=f"by {truncate_text(book.author, 30)}",
            font=("Segoe UI", 9),
            bg=row_color,
            fg="#666666"
        ).pack(side=tk.LEFT)

        tk.Label(
            details_frame,
            text=f" • {book.genre}",
            font=("Segoe UI", 8),
            bg=row_color,
            fg="#666666"
        ).pack(side=tk.LEFT, padx=(5, 0))

        # Status badge (middle)
        status_frame = tk.Frame(row, bg=row_color)
        status_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20)

        status_badge = tk.Label(
            status_frame,
            text=book.status,
            font=("Segoe UI", 9, "bold"),
            bg=STATUS_COLORS.get(book.status, COLORS["light"]),
            fg="white",
            padx=10,
            pady=2
        )
        status_badge.pack(anchor="center", pady=20)

        # Rating (middle)
        rating_frame = tk.Frame(row, bg=row_color)
        rating_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20)

        if book.rating > 0:
            stars = get_star_rating(book.rating)
            tk.Label(
                rating_frame,
                text=stars,
                font=("Segoe UI", 12),
                bg=row_color,
                fg=COLORS["warning"]
            ).pack(anchor="center", pady=20)
        else:
            tk.Label(
                rating_frame,
                text="No rating",
                font=("Segoe UI", 9),
                bg=row_color,
                fg="#999999"
            ).pack(anchor="center", pady=20)

        # Progress (right)
        progress_frame = tk.Frame(row, bg=row_color)
        progress_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20)

        if book.status == "Reading":
            progress_text = f"{book.progress}%"
            progress_color = COLORS["primary"]
        elif book.status == "Completed":
            progress_text = "100%"
            progress_color = COLORS["success"]
        else:
            progress_text = book.status
            progress_color = COLORS["light"]

        tk.Label(
            progress_frame,
            text=progress_text,
            font=("Segoe UI", 11, "bold"),
            bg=row_color,
            fg=progress_color
        ).pack(anchor="center", pady=20)

        # View button (far right)
        button_frame = tk.Frame(row, bg=row_color)
        button_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=20)

        view_button = tk.Button(
            button_frame,
            text="View",
            font=("Segoe UI", 9),
            bg=COLORS["primary"],
            fg="white",
            activebackground=COLORS["secondary"],
            activeforeground="white",
            relief="flat",
            padx=15,
            pady=3,
            cursor="hand2",
            command=lambda b=book: BookDetailsDialog(self.app.root, b, self.app)
        )
        view_button.pack(anchor="center", pady=20)

        return row

    def show_empty_results(self):
        """Show empty results message"""
        empty_frame = tk.Frame(self.results_frame, bg=COLORS["background"])
        empty_frame.pack(fill=tk.BOTH, expand=True, pady=100)

        tk.Label(
            empty_frame,
            text="🔍",
            font=("Segoe UI", 72),
            bg=COLORS["background"],
            fg=COLORS["light"]
        ).pack()

        tk.Label(
            empty_frame,
            text="No books found",
            font=("Segoe UI", 16),
            bg=COLORS["background"],
            fg=COLORS["text"]
        ).pack(pady=10)

        tk.Label(
            empty_frame,
            text="Try different search terms or filters",
            font=("Segoe UI", 12),
            bg=COLORS["background"],
            fg=COLORS["text"]
        ).pack()

        # Clear filters button
        clear_button = tk.Button(
            empty_frame,
            text="Clear All Filters",
            font=("Segoe UI", 11),
            bg=COLORS["light"],
            fg=COLORS["text"],
            activebackground=COLORS["accent"],
            activeforeground=COLORS["text"],
            relief="flat",
            padx=20,
            pady=8,
            cursor="hand2",
            command=self.clear_search
        )
        clear_button.pack(pady=20)

    def clear_search(self):
        """Clear all search filters"""
        self.search_query.set("")
        self.status_filter.set("All")
        self.category_filter.set("All")
        self.rating_filter.set("0")

        # Perform empty search to show all books
        self.perform_search()

    def refresh(self):
        """Refresh search tab"""
        # Update category dropdown
        self.perform_search()

    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")