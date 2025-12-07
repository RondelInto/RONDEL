import tkinter as tk
from tkinter import ttk
import sys
import os
import platform  # For cross-platform mouse wheel handling

# Adjust path for imports (retains original logic)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from config import COLORS, STATUS_COLORS
except ImportError as e:
    print(f"Error importing config: {e}. Using default colors.")
    COLORS = {
        "background": "#f5f5f5",
        "text": "#000000",
        "primary": "#4B0082",
        "secondary": "#7A3BA3",
        "light": "#cccccc"
    }
    STATUS_COLORS = {
        "Reading": "#007bff",
        "Completed": "#28a745",
        "On Hold": "#ffc107",
        "Not Started": "#6c757d"
    }

try:
    from components.widgets.book_card import BookCard
except ImportError as e:
    print(f"Error importing BookCard: {e}. Book display will be disabled.")
    BookCard = None  # Fallback to disable book cards

class LibraryTab:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app

        # Create main frame
        self.frame = tk.Frame(parent, bg=COLORS["background"])

        # Variables for filtering and sorting
        self.status_filter = tk.StringVar(value="All")
        self.sort_by = tk.StringVar(value="Title")
        self.search_query = tk.StringVar(value="")

        # Current books display
        self.current_books = []

        self.create_widgets()

    def create_widgets(self):
        """Create all widgets for library tab"""
        try:
            # Create main container
            main_container = tk.Frame(self.frame, bg=COLORS["background"])
            main_container.pack(fill=tk.BOTH, expand=True)

            # Create top control panel
            self.create_control_panel(main_container)

            # Create books display area
            self.create_books_display(main_container)
        except Exception as e:
            print(f"Error creating widgets: {e}")
            # Fallback: Show error message
            error_label = tk.Label(self.frame, text=f"Error loading library tab: {e}", bg=COLORS["background"], fg="red")
            error_label.pack(pady=20)

    def create_control_panel(self, parent):
        """Create control panel with filters and search"""
        control_frame = tk.Frame(parent, bg=COLORS["background"])
        control_frame.pack(fill=tk.X, padx=20, pady=(10, 0))

        # Search bar
        search_frame = tk.Frame(control_frame, bg=COLORS["background"])
        search_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

        tk.Label(
            search_frame,
            text="🔍",
            font=("Segoe UI", 14),
            bg=COLORS["background"],
            fg=COLORS["text"]
        ).pack(side=tk.LEFT, padx=(0, 10))

        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_query,
            font=("Segoe UI", 11),
            bg="white",
            fg=COLORS["text"],
            relief="solid",
            borderwidth=1,
            width=30
        )
        search_entry.pack(side=tk.LEFT, padx=(0, 10))
        search_entry.bind("<KeyRelease>", lambda e: self.filter_books())

        # Status filter
        filter_frame = tk.Frame(control_frame, bg=COLORS["background"])
        filter_frame.pack(side=tk.LEFT, padx=(20, 0))

        tk.Label(
            filter_frame,
            text="Status:",
            font=("Segoe UI", 10, "bold"),
            bg=COLORS["background"],
            fg=COLORS["text"]
        ).pack(side=tk.LEFT, padx=(0, 10))

        statuses = ["All", "Reading", "Completed", "On Hold", "Not Started"]
        for status in statuses:
            rb = tk.Radiobutton(
                filter_frame,
                text=status,
                variable=self.status_filter,
                value=status,
                command=self.filter_books,
                bg=COLORS["background"],
                fg=COLORS["text"],
                selectcolor=COLORS["background"],
                activebackground=COLORS["background"],
                font=("Segoe UI", 9)
            )
            rb.pack(side=tk.LEFT, padx=5)

        # Sort options
        sort_frame = tk.Frame(control_frame, bg=COLORS["background"])
        sort_frame.pack(side=tk.RIGHT)

        tk.Label(
            sort_frame,
            text="Sort:",
            font=("Segoe UI", 10, "bold"),
            bg=COLORS["background"],
            fg=COLORS["text"]
        ).pack(side=tk.LEFT, padx=(0, 10))

        sort_options = ["Title", "Author", "Progress", "Rating", "Recently Added"]
        sort_menu = ttk.Combobox(
            sort_frame,
            textvariable=self.sort_by,
            values=sort_options,
            state="readonly",
            width=15,
            font=("Segoe UI", 9)
        )
        sort_menu.pack(side=tk.LEFT)
        sort_menu.bind("<<ComboboxSelected>>", lambda e: self.sort_books())

    def create_books_display(self, parent):
        """Create scrollable area for book cards"""
        # Create container for books grid
        books_container = tk.Frame(parent, bg=COLORS["background"])
        books_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Create canvas for scrolling
        self.canvas = tk.Canvas(
            books_container,
            bg=COLORS["background"],
            highlightthickness=0
        )
        scrollbar = ttk.Scrollbar(
            books_container,
            orient="vertical",
            command=self.canvas.yview
        )

        # Create scrollable frame
        self.scrollable_frame = tk.Frame(self.canvas, bg=COLORS["background"])
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Create window in canvas
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Pack canvas and scrollbar
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind mouse wheel
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def filter_books(self):
        """Filter books based on current criteria"""
        query = self.search_query.get().lower().strip()
        status = self.status_filter.get()

        try:
            # Get all books (safe call)
            if not hasattr(self.app, 'book_service') or not hasattr(self.app.book_service, 'get_all_books'):
                raise AttributeError("book_service or get_all_books method not found.")
            all_books = self.app.book_service.get_all_books()
        except Exception as e:
            print(f"Error fetching books: {e}")
            all_books = []

        # Apply filters
        filtered_books = []
        for book in all_books:
            try:
                # Status filter (safe access)
                book_status = getattr(book, 'status', 'Unknown')
                if status != "All" and book_status != status:
                    continue

                # Search query filter (safe access)
                if query:
                    search_fields = [
                        getattr(book, 'title', '').lower(),
                        getattr(book, 'author', '').lower(),
                        getattr(book, 'genre', '').lower(),
                        getattr(book, 'isbn', '')
                    ]
                    if not any(query in field for field in search_fields):
                        continue

                filtered_books.append(book)
            except Exception as e:
                print(f"Error filtering book {book}: {e}")
                continue

        # Sort books
        self.current_books = self.sort_books_list(filtered_books)

        # Display books
        self.display_books()

    def sort_books(self):
        """Sort current books"""
        self.current_books = self.sort_books_list(self.current_books)
        self.display_books()

    def sort_books_list(self, books):
        """Sort books based on current sort criteria"""
        sort_criteria = self.sort_by.get()

        try:
            if sort_criteria == "Title":
                return sorted(books, key=lambda x: getattr(x, 'title', '').lower())
            elif sort_criteria == "Author":
                return sorted(books, key=lambda x: getattr(x, 'author', '').lower())
            elif sort_criteria == "Progress":
                return sorted(books, key=lambda x: getattr(x, 'progress', 0) if isinstance(getattr(x, 'progress', 0), (int, float)) else 0, reverse=True)
            elif sort_criteria == "Rating":
                return sorted(books, key=lambda x: getattr(x, 'rating', 0) if isinstance(getattr(x, 'rating', 0), (int, float)) else 0, reverse=True)
            elif sort_criteria == "Recently Added":
                return list(reversed(books))  # Assumes original order is by addition
            else:
                return books
        except Exception as e:
            print(f"Error sorting books: {e}")
            return books

    def display_books(self):
        """Display books in grid layout"""
        # Clear existing books
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        if not self.current_books:
            self.show_empty_state()
            return

        # Display books in grid (4 columns)
        for i, book in enumerate(self.current_books):
            try:
                row = i // 4
                col = i % 4

                # Create book card (only if BookCard is available)
                if BookCard:
                    book_card = BookCard(self.scrollable_frame, book, self.app)
                    book_card.frame.grid(
                        row=row,
                        column=col,
                        padx=10,
                        pady=10,
                        sticky="nsew"
                    )

                    # Configure grid weights
                    self.scrollable_frame.grid_columnconfigure(col, weight=1)
                    self.scrollable_frame.grid_rowconfigure(row, weight=1)
                else:
                    # Fallback: Show text label if BookCard failed to import
                    tk.Label(self.scrollable_frame, text=f"Book: {getattr(book, 'title', 'Unknown')}", bg=COLORS["background"]).grid(row=row, column=col, padx=10, pady=10)
            except Exception as e:
                print(f"Error displaying book {book}: {e}")
                continue

    def show_empty_state(self):
        """Show empty library message"""
        empty_frame = tk.Frame(self.scrollable_frame, bg=COLORS["background"])
        empty_frame.pack(fill=tk.BOTH, expand=True, pady=100)

        tk.Label(
            empty_frame,
            text="📚",
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
            text="Add some books to get started!",
            font=("Segoe UI", 12),
            bg=COLORS["background"],
            fg=COLORS["text"]
        ).pack()

        add_button = tk.Button(
            empty_frame,
            text="➕ Add Your First Book",
            font=("Segoe UI", 11, "bold"),
            bg=COLORS["primary"],
            fg="white",
            activebackground=COLORS["secondary"],
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2",
            command=lambda: self._safe_call_show_add_book()
        )
        add_button.pack(pady=20)

    def _safe_call_show_add_book(self):
        """Safely call show_add_book if available"""
        try:
            if hasattr(self.app, 'show_add_book') and callable(getattr(self.app, 'show_add_book')):
                self.app.show_add_book()
            else:
                print("show_add_book method not available.")
        except Exception as e:
            print(f"Error calling show_add_book: {e}")

    def refresh(self):
        """Refresh library display"""
        self.filter_books()

    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling (cross-platform)"""
        try:
            if platform.system() == "Windows":
                self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            else:
                # For Linux/Mac, delta might be different
                self.canvas.yview_scroll(-1 if event.delta > 0 else 1, "units")
        except Exception as e:
            print(f"Error handling mouse wheel: {e}")
