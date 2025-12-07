# components/add_book_tab.py
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from config import COLORS
from models import Book
from utils.helpers import generate_id
from utils.validators import validate_isbn, validate_year, validate_pages, validate_rating
from datetime import datetime


class AddBookTab:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.frame = tk.Frame(parent, bg=COLORS["background"])

        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Create tabs
        self.create_manual_entry_tab()
        self.create_search_online_tab()

    def create_manual_entry_tab(self):
        """Create manual book entry tab"""
        manual_frame = tk.Frame(self.notebook, bg=COLORS["background"])
        self.notebook.add(manual_frame, text="✏️ Manual Entry")

        # Title
        title_label = tk.Label(
            manual_frame,
            text="Add New Book",
            font=("Segoe UI", 20, "bold"),
            bg=COLORS["background"],
            fg=COLORS["primary"]
        )
        title_label.pack(pady=(20, 10))

        # Create scrollable form
        container = tk.Frame(manual_frame, bg=COLORS["background"])
        container.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(container, bg=COLORS["background"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        form_frame = tk.Frame(canvas, bg=COLORS["background"])

        form_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=form_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Form fields
        self.create_manual_form(form_frame)

    def create_manual_form(self, parent):
        """Create manual entry form"""
        # Form container
        form_container = tk.Frame(parent, bg=COLORS["background"])
        form_container.pack(fill=tk.BOTH, expand=True, padx=50, pady=20)

        # Store form fields
        self.form_fields = {}

        # Basic Information Section
        basic_frame = tk.LabelFrame(
            form_container,
            text="Basic Information",
            font=("Segoe UI", 12, "bold"),
            bg=COLORS["background"],
            fg=COLORS["primary"],
            relief="solid",
            borderwidth=1,
            padx=15,
            pady=15
        )
        basic_frame.pack(fill=tk.X, pady=(0, 20))

        # Title
        title_frame = tk.Frame(basic_frame, bg=COLORS["background"])
        title_frame.pack(fill=tk.X, pady=5)

        tk.Label(
            title_frame,
            text="Title *",
            font=("Segoe UI", 10, "bold"),
            bg=COLORS["background"],
            fg=COLORS["text"],
            width=15,
            anchor="w"
        ).pack(side=tk.LEFT)

        self.form_fields["title"] = tk.Entry(
            title_frame,
            font=("Segoe UI", 10),
            width=40
        )
        self.form_fields["title"].pack(side=tk.LEFT)

        # Author
        author_frame = tk.Frame(basic_frame, bg=COLORS["background"])
        author_frame.pack(fill=tk.X, pady=5)

        tk.Label(
            author_frame,
            text="Author *",
            font=("Segoe UI", 10, "bold"),
            bg=COLORS["background"],
            fg=COLORS["text"],
            width=15,
            anchor="w"
        ).pack(side=tk.LEFT)

        self.form_fields["author"] = tk.Entry(
            author_frame,
            font=("Segoe UI", 10),
            width=40
        )
        self.form_fields["author"].pack(side=tk.LEFT)

        # Publisher
        publisher_frame = tk.Frame(basic_frame, bg=COLORS["background"])
        publisher_frame.pack(fill=tk.X, pady=5)

        tk.Label(
            publisher_frame,
            text="Publisher",
            font=("Segoe UI", 10, "bold"),
            bg=COLORS["background"],
            fg=COLORS["text"],
            width=15,
            anchor="w"
        ).pack(side=tk.LEFT)

        self.form_fields["publisher"] = tk.Entry(
            publisher_frame,
            font=("Segoe UI", 10),
            width=40
        )
        self.form_fields["publisher"].pack(side=tk.LEFT)

        # Genre
        genre_frame = tk.Frame(basic_frame, bg=COLORS["background"])
        genre_frame.pack(fill=tk.X, pady=5)

        tk.Label(
            genre_frame,
            text="Genre",
            font=("Segoe UI", 10, "bold"),
            bg=COLORS["background"],
            fg=COLORS["text"],
            width=15,
            anchor="w"
        ).pack(side=tk.LEFT)

        self.form_fields["genre"] = tk.Entry(
            genre_frame,
            font=("Segoe UI", 10),
            width=40
        )
        self.form_fields["genre"].pack(side=tk.LEFT)

        # ISBN
        isbn_frame = tk.Frame(basic_frame, bg=COLORS["background"])
        isbn_frame.pack(fill=tk.X, pady=5)

        tk.Label(
            isbn_frame,
            text="ISBN",
            font=("Segoe UI", 10, "bold"),
            bg=COLORS["background"],
            fg=COLORS["text"],
            width=15,
            anchor="w"
        ).pack(side=tk.LEFT)

        self.form_fields["isbn"] = tk.Entry(
            isbn_frame,
            font=("Segoe UI", 10),
            width=40
        )
        self.form_fields["isbn"].pack(side=tk.LEFT)

        # Year
        year_frame = tk.Frame(basic_frame, bg=COLORS["background"])
        year_frame.pack(fill=tk.X, pady=5)

        tk.Label(
            year_frame,
            text="Publication Year",
            font=("Segoe UI", 10, "bold"),
            bg=COLORS["background"],
            fg=COLORS["text"],
            width=15,
            anchor="w"
        ).pack(side=tk.LEFT)

        self.form_fields["year"] = tk.Entry(
            year_frame,
            font=("Segoe UI", 10),
            width=40
        )
        self.form_fields["year"].insert(0, str(datetime.now().year))
        self.form_fields["year"].pack(side=tk.LEFT)

        # Description Section
        desc_frame = tk.LabelFrame(
            form_container,
            text="Description",
            font=("Segoe UI", 12, "bold"),
            bg=COLORS["background"],
            fg=COLORS["primary"],
            relief="solid",
            borderwidth=1,
            padx=15,
            pady=15
        )
        desc_frame.pack(fill=tk.X, pady=(0, 20))

        self.form_fields["description"] = scrolledtext.ScrolledText(
            desc_frame,
            font=("Segoe UI", 10),
            height=6,
            bg="white",
            fg=COLORS["text"],
            relief="solid",
            borderwidth=1
        )
        self.form_fields["description"].pack(fill=tk.X)

        # Reading Status Section
        status_frame = tk.LabelFrame(
            form_container,
            text="Reading Status",
            font=("Segoe UI", 12, "bold"),
            bg=COLORS["background"],
            fg=COLORS["primary"],
            relief="solid",
            borderwidth=1,
            padx=15,
            pady=15
        )
        status_frame.pack(fill=tk.X, pady=(0, 20))

        # Status selection
        self.status_var = tk.StringVar(value="Not Started")

        status_options = [
            ("Not Started", "Not Started"),
            ("Reading", "Reading"),
            ("Completed", "Completed"),
            ("On Hold", "On Hold")
        ]

        for text, value in status_options:
            rb = tk.Radiobutton(
                status_frame,
                text=text,
                variable=self.status_var,
                value=value,
                bg=COLORS["background"],
                fg=COLORS["text"],
                selectcolor=COLORS["background"],
                activebackground=COLORS["background"],
                font=("Segoe UI", 10)
            )
            rb.pack(anchor="w", pady=2)

        # Pages information
        pages_frame = tk.Frame(status_frame, bg=COLORS["background"])
        pages_frame.pack(fill=tk.X, pady=(10, 0))

        tk.Label(
            pages_frame,
            text="Pages:",
            font=("Segoe UI", 10, "bold"),
            bg=COLORS["background"],
            fg=COLORS["text"]
        ).pack(side=tk.LEFT, padx=(0, 10))

        tk.Label(
            pages_frame,
            text="Current:",
            font=("Segoe UI", 9),
            bg=COLORS["background"],
            fg=COLORS["text"]
        ).pack(side=tk.LEFT)

        self.form_fields["current_page"] = tk.Entry(
            pages_frame,
            font=("Segoe UI", 10),
            width=8
        )
        self.form_fields["current_page"].insert(0, "0")
        self.form_fields["current_page"].pack(side=tk.LEFT, padx=(5, 20))

        tk.Label(
            pages_frame,
            text="Total:",
            font=("Segoe UI", 9),
            bg=COLORS["background"],
            fg=COLORS["text"]
        ).pack(side=tk.LEFT)

        self.form_fields["total_pages"] = tk.Entry(
            pages_frame,
            font=("Segoe UI", 10),
            width=8
        )
        self.form_fields["total_pages"].insert(0, "0")
        self.form_fields["total_pages"].pack(side=tk.LEFT, padx=5)

        # Categories Section
        categories_frame = tk.LabelFrame(
            form_container,
            text="Categories",
            font=("Segoe UI", 12, "bold"),
            bg=COLORS["background"],
            fg=COLORS["primary"],
            relief="solid",
            borderwidth=1,
            padx=15,
            pady=15
        )
        categories_frame.pack(fill=tk.X, pady=(0, 20))

        # Category selection
        self.category_vars = {}
        try:
            categories = []
            if getattr(self.app, 'category_service', None) and hasattr(self.app.category_service, 'get_all_categories'):
                categories = self.app.category_service.get_all_categories() or []
            else:
                # fallback to shared services package
                try:
                    import services as services_pkg
                    if getattr(services_pkg, 'category_service', None):
                        categories = services_pkg.category_service.get_all_categories() or []
                except Exception:
                    categories = []
        except Exception:
            categories = []

        for category in categories:
            name = getattr(category, 'name', str(category))
            var = tk.BooleanVar(value=False)
            self.category_vars[name] = var

            cb = tk.Checkbutton(
                categories_frame,
                text=name,
                variable=var,
                bg=COLORS["background"],
                fg=COLORS["text"],
                selectcolor=COLORS["background"],
                activebackground=COLORS["background"],
                font=("Segoe UI", 10)
            )
            cb.pack(anchor="w", pady=2)

        # Submit button
        submit_frame = tk.Frame(form_container, bg=COLORS["background"])
        submit_frame.pack(pady=20)

        submit_button = tk.Button(
            submit_frame,
            text="➕ Add Book to Library",
            font=("Segoe UI", 12, "bold"),
            bg=COLORS["success"],
            fg="white",
            activebackground=COLORS["success"],
            activeforeground="white",
            relief="flat",
            padx=30,
            pady=12,
            cursor="hand2",
            command=self.submit_manual_book
        )
        submit_button.pack()

    def create_search_online_tab(self):
        """Create online search tab"""
        search_frame = tk.Frame(self.notebook, bg=COLORS["background"])
        self.notebook.add(search_frame, text="🔍 Search Online")

        # Title
        title_label = tk.Label(
            search_frame,
            text="Search for Books Online",
            font=("Segoe UI", 20, "bold"),
            bg=COLORS["background"],
            fg=COLORS["primary"]
        )
        title_label.pack(pady=(20, 10))

        # Search box
        search_container = tk.Frame(search_frame, bg=COLORS["background"])
        search_container.pack(fill=tk.X, padx=50, pady=20)

        tk.Label(
            search_container,
            text="Search by ISBN, Title, or Author:",
            font=("Segoe UI", 11),
            bg=COLORS["background"],
            fg=COLORS["text"]
        ).pack(anchor="w", pady=(0, 10))

        search_box_frame = tk.Frame(search_container, bg=COLORS["background"])
        search_box_frame.pack(fill=tk.X)

        self.search_entry = tk.Entry(
            search_box_frame,
            font=("Segoe UI", 12),
            width=40
        )
        self.search_entry.pack(side=tk.LEFT, padx=(0, 10))

        search_button = tk.Button(
            search_box_frame,
            text="Search",
            font=("Segoe UI", 10, "bold"),
            bg=COLORS["primary"],
            fg="white",
            activebackground=COLORS["secondary"],
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=5,
            cursor="hand2",
            command=self.search_online
        )
        search_button.pack(side=tk.LEFT)

        # Results area
        results_frame = tk.Frame(search_frame, bg=COLORS["background"])
        results_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        tk.Label(
            results_frame,
            text="Search Results:",
            font=("Segoe UI", 12, "bold"),
            bg=COLORS["background"],
            fg=COLORS["text"]
        ).pack(anchor="w", pady=(0, 10))

        # Create canvas for results
        self.results_canvas = tk.Canvas(
            results_frame,
            bg=COLORS["background"],
            highlightthickness=0
        )
        scrollbar = ttk.Scrollbar(
            results_frame,
            orient="vertical",
            command=self.results_canvas.yview
        )

        self.results_frame = tk.Frame(self.results_canvas, bg=COLORS["background"])
        self.results_frame.bind(
            "<Configure>",
            lambda e: self.results_canvas.configure(scrollregion=self.results_canvas.bbox("all"))
        )

        self.results_canvas.create_window((0, 0), window=self.results_frame, anchor="nw")
        self.results_canvas.configure(yscrollcommand=scrollbar.set)

        self.results_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def search_online(self):
        """Search for books online (simulated)"""
        query = self.search_entry.get().strip()

        if not query:
            messagebox.showwarning("Empty Search", "Please enter a search term")
            return

        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        # Simulate API search with sample results
        from utils.sample_data import generate_sample_books
        sample_books = generate_sample_books(3)

        # Filter by query (simulated)
        filtered_books = [
            book for book in sample_books
            if query.lower() in book.title.lower() or
               query.lower() in book.author.lower() or
               query in book.isbn
        ]

        if not filtered_books:
            # Show no results message
            no_results_frame = tk.Frame(
                self.results_frame,
                bg=COLORS["background"]
            )
            no_results_frame.pack(fill=tk.BOTH, expand=True, pady=50)

            tk.Label(
                no_results_frame,
                text="🔍",
                font=("Segoe UI", 48),
                bg=COLORS["background"],
                fg=COLORS["light"]
            ).pack()

            tk.Label(
                no_results_frame,
                text="No books found",
                font=("Segoe UI", 14),
                bg=COLORS["background"],
                fg=COLORS["text"]
            ).pack(pady=10)

            tk.Label(
                no_results_frame,
                text="Try a different search term",
                font=("Segoe UI", 12),
                bg=COLORS["background"],
                fg=COLORS["text"]
            ).pack()

            return

        # Display results
        for i, book in enumerate(filtered_books):
            result_card = self.create_search_result_card(book)
            result_card.pack(fill=tk.X, pady=5)

    def create_search_result_card(self, book):
        """Create a search result card"""
        card = tk.Frame(
            self.results_frame,
            bg="white",
            relief="solid",
            borderwidth=1
        )

        # Book info frame
        info_frame = tk.Frame(card, bg="white")
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=15)

        # Title
        tk.Label(
            info_frame,
            text=book.title,
            font=("Segoe UI", 14, "bold"),
            bg="white",
            fg=COLORS["text"]
        ).pack(anchor="w")

        # Author and details
        details_frame = tk.Frame(info_frame, bg="white")
        details_frame.pack(anchor="w", pady=5)

        tk.Label(
            details_frame,
            text=f"by {book.author}",
            font=("Segoe UI", 11),
            bg="white",
            fg="#666666"
        ).pack(side=tk.LEFT)

        tk.Label(
            details_frame,
            text=f" • {book.publisher}, {book.year}",
            font=("Segoe UI", 10),
            bg="white",
            fg="#666666"
        ).pack(side=tk.LEFT, padx=(10, 0))

        # Description
        tk.Label(
            info_frame,
            text=book.description[:150] + "...",
            font=("Segoe UI", 9),
            bg="white",
            fg="#666666",
            wraplength=600,
            justify="left"
        ).pack(anchor="w", pady=(5, 0))

        # Add button
        button_frame = tk.Frame(card, bg="white")
        button_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=20)

        add_button = tk.Button(
            button_frame,
            text="Add to Library",
            font=("Segoe UI", 10, "bold"),
            bg=COLORS["success"],
            fg="white",
            activebackground=COLORS["success"],
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=8,
            cursor="hand2",
            command=lambda b=book: self.add_searched_book(b)
        )
        add_button.pack(anchor="center", pady=50)

        return card

    def add_searched_book(self, book):
        """Add searched book to library"""
        # Add the book
        self.app.book_service.add_book(book.to_dict())

        # Switch to library tab
        self.app.show_library()

        # Show success message
        messagebox.showinfo(
            "Success",
            f"'{book.title}' has been added to your library!"
        )

    def submit_manual_book(self):
        """Submit manual book entry"""
        # Get form values
        title = self.form_fields["title"].get().strip()
        author = self.form_fields["author"].get().strip()
        publisher = self.form_fields["publisher"].get().strip()
        genre = self.form_fields["genre"].get().strip()
        isbn = self.form_fields["isbn"].get().strip()
        year_str = self.form_fields["year"].get().strip()
        description = self.form_fields["description"].get("1.0", tk.END).strip()
        current_page_str = self.form_fields["current_page"].get().strip()
        total_pages_str = self.form_fields["total_pages"].get().strip()

        # Get selected categories
        selected_categories = ["General"]
        for category_name, var in self.category_vars.items():
            if var.get():
                selected_categories.append(category_name)

        # Validate required fields
        if not title or not author:
            messagebox.showerror(
                "Validation Error",
                "Title and Author are required fields"
            )
            return

        # Validate year
        year_valid, year_msg = validate_year(year_str)
        if not year_valid:
            messagebox.showerror("Validation Error", year_msg)
            return

        # Validate pages
        pages_valid, pages_msg = validate_pages(current_page_str, total_pages_str)
        if not pages_valid:
            messagebox.showerror("Validation Error", pages_msg)
            return

        # Validate ISBN if provided
        if isbn:
            isbn_valid, isbn_msg = validate_isbn(isbn)
            if not isbn_valid:
                response = messagebox.askyesno(
                    "ISBN Warning",
                    f"{isbn_msg}\n\nDo you want to continue anyway?"
                )
                if not response:
                    return

        # Create book data
        book_data = {
            "title": title,
            "author": author,
            "publisher": publisher,
            "genre": genre if genre else "General",
            "isbn": isbn,
            "year": int(year_str),
            "status": self.status_var.get(),
            "description": description,
            "current_page": int(current_page_str),
            "total_pages": int(total_pages_str),
            "categories": selected_categories
        }

        # Add book to library
        try:
            self.app.book_service.add_book(book_data)

            # Clear form
            self.clear_form()

            # Switch to library tab
            self.app.show_library()

            # Show success message
            messagebox.showinfo(
                "Success",
                f"'{title}' has been added to your library!"
            )

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Failed to add book: {str(e)}"
            )

    def clear_form(self):
        """Clear all form fields"""
        for key, field in self.form_fields.items():
            if isinstance(field, tk.Entry):
                field.delete(0, tk.END)
            elif isinstance(field, scrolledtext.ScrolledText):
                field.delete("1.0", tk.END)

        # Reset status
        self.status_var.set("Not Started")

        # Reset categories
        for var in self.category_vars.values():
            var.set(False)

        # Reset year to current year
        self.form_fields["year"].delete(0, tk.END)
        self.form_fields["year"].insert(0, str(datetime.now().year))

        # Reset pages
        self.form_fields["current_page"].delete(0, tk.END)
        self.form_fields["current_page"].insert(0, "0")
        self.form_fields["total_pages"].delete(0, tk.END)
        self.form_fields["total_pages"].insert(0, "0")

    def refresh(self):
        """Refresh the tab (update categories, etc.)"""
        # Update categories in form
        try:
            # rebuild category checkboxes
            # find categories_frame by walking children (best-effort)
            for child in self.frame.winfo_children():
                # notebook is first child
                if isinstance(child, ttk.Notebook):
                    # manual tab frame is first tab
                    tabs = child.winfo_children()
                    if tabs:
                        manual_frame = tabs[0]
                        # search for categories_frame inside manual_frame
                        for w in manual_frame.winfo_children():
                            # we rely on naming/structure, so simply recreate form fields
                            pass
        except Exception:
            pass