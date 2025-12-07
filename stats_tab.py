# components/stats_tab.py
import tkinter as tk
from tkinter import ttk
from config import COLORS
from components.widgets.kpi_card import KPICard
from components.widgets.achievement_card import AchievementCard
import random


class StatsTab:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.frame = tk.Frame(parent, bg=COLORS["background"])

        # Statistics data
        self.stats_data = {}
        self.kpi_cards = []
        self.achievements = []

        self.create_widgets()

    def create_widgets(self):
        """Create all widgets for stats tab"""
        # Create main container with scroll
        main_container = tk.Frame(self.frame, bg=COLORS["background"])
        main_container.pack(fill=tk.BOTH, expand=True)

        # Create scrollable canvas
        self.canvas = tk.Canvas(
            main_container,
            bg=COLORS["background"],
            highlightthickness=0
        )
        scrollbar = ttk.Scrollbar(
            main_container,
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

        # Title
        title_label = tk.Label(
            self.scrollable_frame,
            text="📊 Reading Statistics Dashboard",
            font=("Segoe UI", 24, "bold"),
            bg=COLORS["background"],
            fg=COLORS["primary"]
        )
        title_label.pack(pady=(20, 10))

        # KPI Cards Section
        self.create_kpi_section()

        # Achievements Section
        self.create_achievements_section()

        # Charts Section
        self.create_charts_section()

    def create_kpi_section(self):
        """Create KPI cards section"""
        # Section header
        section_frame = tk.Frame(self.scrollable_frame, bg=COLORS["background"])
        section_frame.pack(fill=tk.X, padx=20, pady=(0, 10))

        tk.Label(
            section_frame,
            text="Key Performance Indicators",
            font=("Segoe UI", 18, "bold"),
            bg=COLORS["background"],
            fg=COLORS["primary"]
        ).pack(anchor="w", pady=(0, 10))

        # KPI Cards container
        self.kpi_container = tk.Frame(self.scrollable_frame, bg=COLORS["background"])
        self.kpi_container.pack(fill=tk.X, padx=20, pady=(0, 20))

        # Will be populated in refresh()

    def create_achievements_section(self):
        """Create achievements section"""
        # Section header
        section_frame = tk.Frame(self.scrollable_frame, bg=COLORS["background"])
        section_frame.pack(fill=tk.X, padx=20, pady=(0, 10))

        tk.Label(
            section_frame,
            text="🏆 Achievements",
            font=("Segoe UI", 18, "bold"),
            bg=COLORS["background"],
            fg=COLORS["primary"]
        ).pack(anchor="w", pady=(0, 10))

        # Achievements container
        self.achievements_container = tk.Frame(
            self.scrollable_frame,
            bg=COLORS["background"]
        )
        self.achievements_container.pack(fill=tk.X, padx=20, pady=(0, 20))

        # Will be populated in refresh()

    def create_charts_section(self):
        """Create charts section"""
        # Section header
        section_frame = tk.Frame(self.scrollable_frame, bg=COLORS["background"])
        section_frame.pack(fill=tk.X, padx=20, pady=(0, 10))

        tk.Label(
            section_frame,
            text="📈 Reading Insights",
            font=("Segoe UI", 18, "bold"),
            bg=COLORS["background"],
            fg=COLORS["primary"]
        ).pack(anchor="w", pady=(0, 10))

        # Charts container
        charts_container = tk.Frame(self.scrollable_frame, bg=COLORS["background"])
        charts_container.pack(fill=tk.X, padx=20, pady=(0, 30))

        # Create two chart frames side by side
        left_chart_frame = tk.Frame(charts_container, bg=COLORS["background"])
        left_chart_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        right_chart_frame = tk.Frame(charts_container, bg=COLORS["background"])
        right_chart_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        # Genre distribution chart
        self.create_genre_chart(left_chart_frame)

        # Reading progress chart
        self.create_progress_chart(right_chart_frame)

    def create_genre_chart(self, parent):
        """Create genre distribution chart"""
        chart_frame = tk.Frame(
            parent,
            bg="white",
            relief="solid",
            borderwidth=1
        )
        chart_frame.pack(fill=tk.BOTH, expand=True)

        # Chart title
        tk.Label(
            chart_frame,
            text="Genre Distribution",
            font=("Segoe UI", 14, "bold"),
            bg="white",
            fg=COLORS["text"]
        ).pack(pady=(15, 10))

        # Create canvas for chart
        chart_canvas = tk.Canvas(
            chart_frame,
            bg="white",
            height=250,
            highlightthickness=0
        )
        chart_canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Draw chart (simulated)
        self.draw_genre_chart(chart_canvas)

    def create_progress_chart(self, parent):
        """Create reading progress chart"""
        chart_frame = tk.Frame(
            parent,
            bg="white",
            relief="solid",
            borderwidth=1
        )
        chart_frame.pack(fill=tk.BOTH, expand=True)

        # Chart title
        tk.Label(
            chart_frame,
            text="Reading Progress",
            font=("Segoe UI", 14, "bold"),
            bg="white",
            fg=COLORS["text"]
        ).pack(pady=(15, 10))

        # Create canvas for chart
        chart_canvas = tk.Canvas(
            chart_frame,
            bg="white",
            height=250,
            highlightthickness=0
        )
        chart_canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Draw chart (simulated)
        self.draw_progress_chart(chart_canvas)

    def draw_genre_chart(self, canvas):
        """Draw genre distribution chart (simulated)"""
        # Sample genre data
        genres = ["Fiction", "Non-Fiction", "Fantasy", "Sci-Fi", "Mystery", "Biography"]
        values = [random.randint(5, 20) for _ in range(len(genres))]

        if not values:
            return

        max_val = max(values)
        bar_width = 30
        spacing = 10
        chart_width = len(genres) * (bar_width + spacing) + 20
        chart_height = 180
        base_y = 200

        colors = [
            COLORS["primary"],
            COLORS["secondary"],
            COLORS["success"],
            COLORS["warning"],
            COLORS["danger"],
            COLORS["info"]
        ]

        for i, (genre, value) in enumerate(zip(genres, values)):
            x = 50 + i * (bar_width + spacing)
            height = (value / max_val) * 150 if max_val > 0 else 0
            y = base_y - height

            # Draw bar
            color = colors[i % len(colors)]
            canvas.create_rectangle(
                x, y, x + bar_width, base_y,
                fill=color,
                outline=color
            )

            # Draw value label
            canvas.create_text(
                x + bar_width / 2, y - 10,
                text=str(value),
                font=("Segoe UI", 9),
                fill=COLORS["text"]
            )

            # Draw genre label
            canvas.create_text(
                x + bar_width / 2, base_y + 15,
                text=genre[:8],
                font=("Segoe UI", 8),
                fill=COLORS["text"],
                angle=45
            )

    def draw_progress_chart(self, canvas):
        """Draw reading progress chart (simulated)"""
        # Sample progress data
        books = ["Book 1", "Book 2", "Book 3", "Book 4", "Book 5"]
        progress = [random.randint(20, 100) for _ in range(len(books))]

        bar_width = 40
        spacing = 20
        chart_width = len(books) * (bar_width + spacing) + 20
        chart_height = 180
        base_y = 200

        for i, (book, prog) in enumerate(zip(books, progress)):
            x = 50 + i * (bar_width + spacing)
            height = (prog / 100) * 150
            y = base_y - height

            # Draw progress bar
            color = COLORS["primary"] if prog < 50 else COLORS["success"]
            canvas.create_rectangle(
                x, y, x + bar_width, base_y,
                fill=color,
                outline=color
            )

            # Draw progress percentage
            canvas.create_text(
                x + bar_width / 2, y - 10,
                text=f"{prog}%",
                font=("Segoe UI", 9),
                fill=COLORS["text"]
            )

            # Draw book label
            canvas.create_text(
                x + bar_width / 2, base_y + 15,
                text=book,
                font=("Segoe UI", 8),
                fill=COLORS["text"]
            )

    def refresh(self):
        """Refresh statistics display"""
        # Get updated statistics (defensive)
        books = []
        try:
            if getattr(self.app, 'book_service', None) and hasattr(self.app.book_service, 'get_all_books'):
                books = self.app.book_service.get_all_books() or []
            else:
                try:
                    import services as services_pkg
                    if getattr(services_pkg, 'book_service', None):
                        books = services_pkg.book_service.get_all_books() or []
                except Exception:
                    books = []
        except Exception:
            books = []

        # store books so other methods can access them
        self.books = books

        # Obtain stats from stats_service, tolerant of dict or object return types
        stats_raw = None
        try:
            if getattr(self.app, 'stats_service', None) and hasattr(self.app.stats_service, 'calculate_statistics'):
                stats_raw = self.app.stats_service.calculate_statistics(books)
            else:
                import services as services_pkg
                if getattr(services_pkg, 'stats_service', None) and hasattr(services_pkg.stats_service, 'calculate_statistics'):
                    stats_raw = services_pkg.stats_service.calculate_statistics(books)
        except Exception:
            stats_raw = None

        # Normalize stats to an object with attributes used by the UI
        class SimpleStats:
            def __init__(self, d=None):
                d = d or {}
                # support dict-like or object-like inputs
                def get(k, default=0):
                    if isinstance(d, dict):
                        return d.get(k, default)
                    return getattr(d, k, default)
                self.total_books = get('total_books', 0)
                self.completed_books = get('completed_books', 0)
                self.reading_books = get('reading_books', 0)
                self.average_progress = get('average_progress', 0)
                self.monthly_completed = get('monthly_completed', 0)
                self.reading_streak = get('reading_streak', 0)
                self.total_pages = get('total_pages', 0)
                self.favorite_genre = get('favorite_genre', 'None')

        if stats_raw is None:
            self.stats_data = SimpleStats()
        elif isinstance(stats_raw, dict):
            self.stats_data = SimpleStats(stats_raw)
        else:
            # assume object with attributes
            try:
                self.stats_data = SimpleStats({
                    'total_books': getattr(stats_raw, 'total_books', 0),
                    'completed_books': getattr(stats_raw, 'completed_books', 0),
                    'reading_books': getattr(stats_raw, 'reading_books', 0),
                    'average_progress': getattr(stats_raw, 'average_progress', 0),
                    'monthly_completed': getattr(stats_raw, 'monthly_completed', 0),
                    'reading_streak': getattr(stats_raw, 'reading_streak', 0),
                    'total_pages': getattr(stats_raw, 'total_pages', 0),
                    'favorite_genre': getattr(stats_raw, 'favorite_genre', 'None')
                })
            except Exception:
                self.stats_data = SimpleStats()

        # Update KPI cards
        self.update_kpi_cards()

        # Update achievements
        self.update_achievements()

    def update_kpi_cards(self):
        """Update KPI cards display"""
        # Clear existing cards
        for widget in self.kpi_container.winfo_children():
            widget.destroy()

        # Create KPI data
        kpis = [
            ("Total Books", self.stats_data.total_books, "📚", COLORS["primary"]),
            ("Completed", self.stats_data.completed_books, "✅", COLORS["success"]),
            ("Reading Now", self.stats_data.reading_books, "📖", COLORS["info"]),
            ("Avg Progress", f"{self.stats_data.average_progress}%", "📈", COLORS["warning"]),
            ("This Month", self.stats_data.monthly_completed, "🗓️", COLORS["secondary"]),
            ("Streak", f"{self.stats_data.reading_streak} days", "🔥", COLORS["danger"]),
            ("Total Pages", self.stats_data.total_pages, "📄", COLORS["accent"]),
            ("Top Genre", self.stats_data.favorite_genre, "🏆", COLORS["success"])
        ]

        # Create KPI cards in grid
        for i, (label, value, icon, color) in enumerate(kpis):
            row = i // 4
            col = i % 4

            # Create KPI card
            kpi_frame = tk.Frame(
                self.kpi_container,
                bg="white",
                relief="solid",
                borderwidth=1
            )
            kpi_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

            # Configure grid weights
            self.kpi_container.grid_columnconfigure(col, weight=1)
            self.kpi_container.grid_rowconfigure(row, weight=1)

            # Icon
            tk.Label(
                kpi_frame,
                text=icon,
                font=("Segoe UI", 24),
                bg="white",
                fg=color
            ).pack(pady=(20, 5))

            # Value
            tk.Label(
                kpi_frame,
                text=str(value),
                font=("Segoe UI", 20, "bold"),
                bg="white",
                fg=COLORS["text"]
            ).pack()

            # Label
            tk.Label(
                kpi_frame,
                text=label,
                font=("Segoe UI", 10),
                bg="white",
                fg=COLORS["text"]
            ).pack(pady=(5, 20))

    def update_achievements(self):
        """Update achievements display"""
        # Clear existing achievements
        for widget in self.achievements_container.winfo_children():
            widget.destroy()

        # use self.books (set in refresh) or fallback to empty list
        books = getattr(self, 'books', []) or []

        # Get achievements from stats/achievement service (normalize)
        try:
            if getattr(self.app, 'stats_service', None) and hasattr(self.app.stats_service, 'check_achievements'):
                achievements = self.app.stats_service.check_achievements(books)
            elif getattr(self.app, 'achievement_service', None) and hasattr(self.app.achievement_service, 'get_achievements'):
                achievements = self.app.achievement_service.get_achievements()
            else:
                import services as services_pkg
                if getattr(services_pkg, 'stats_service', None) and hasattr(services_pkg.stats_service, 'check_achievements'):
                    achievements = services_pkg.stats_service.check_achievements(books)
                elif getattr(services_pkg, 'achievement_service', None) and hasattr(services_pkg.achievement_service, 'get_achievements'):
                    achievements = services_pkg.achievement_service.get_achievements()
                else:
                    achievements = []
        except Exception:
            achievements = []

        # Normalize achievements to objects with expected attributes
        normalized_achievements = []
        for a in (achievements or []):
            if isinstance(a, dict):
                # create simple object
                obj = type('A', (), {})()
                obj.id = a.get('id')
                obj.name = a.get('title') or a.get('name') or a.get('id')
                obj.description = a.get('description', '')
                obj.unlocked = a.get('unlocked', False)
                obj.icon = a.get('icon', '🏆')
                normalized_achievements.append(obj)
            else:
                # assume object-like and try to read fields
                try:
                    obj = a
                    # ensure attributes exist
                    if not hasattr(obj, 'name'):
                        setattr(obj, 'name', getattr(a, 'title', getattr(a, 'id', '')))
                    if not hasattr(obj, 'description'):
                        setattr(obj, 'description', getattr(a, 'description', ''))
                    if not hasattr(obj, 'icon'):
                        setattr(obj, 'icon', getattr(a, 'icon', '🏆'))
                    if not hasattr(obj, 'unlocked'):
                        setattr(obj, 'unlocked', getattr(a, 'unlocked', False))
                    normalized_achievements.append(obj)
                except Exception:
                    continue

        achievements = normalized_achievements

        if not achievements:
            # Show empty state
            empty_frame = tk.Frame(
                self.achievements_container,
                bg=COLORS["background"]
            )
            empty_frame.pack(fill=tk.BOTH, expand=True, pady=50)

            tk.Label(
                empty_frame,
                text="🏆",
                font=("Segoe UI", 48),
                bg=COLORS["background"],
                fg=COLORS["light"]
            ).pack()

            tk.Label(
                empty_frame,
                text="No achievements yet",
                font=("Segoe UI", 14),
                bg=COLORS["background"],
                fg=COLORS["text"]
            ).pack(pady=10)

            return

        # Display achievements in grid
        for i, achievement in enumerate(achievements):
            row = i // 3
            col = i % 3

            # Create achievement card
            achievement_card = tk.Frame(
                self.achievements_container,
                bg="white" if achievement.unlocked else "#f0f0f0",
                relief="solid",
                borderwidth=1,
                width=250,
                height=100
            )
            achievement_card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            achievement_card.grid_propagate(False)

            # Achievement content
            icon_label = tk.Label(
                achievement_card,
                text=achievement.icon,
                font=("Segoe UI", 24),
                bg=achievement_card["bg"],
                fg=COLORS["primary"] if achievement.unlocked else "#cccccc"
            )
            icon_label.place(x=20, y=30)

            # Name
            tk.Label(
                achievement_card,
                text=achievement.name,
                font=("Segoe UI", 12, "bold"),
                bg=achievement_card["bg"],
                fg=COLORS["text"] if achievement.unlocked else "#999999"
            ).place(x=70, y=25)

            # Description
            tk.Label(
                achievement_card,
                text=achievement.description,
                font=("Segoe UI", 9),
                bg=achievement_card["bg"],
                fg=COLORS["text"] if achievement.unlocked else "#999999",
                wraplength=150
            ).place(x=70, y=50)

            # Lock/Unlock indicator
            if not achievement.unlocked:
                tk.Label(
                    achievement_card,
                    text="🔒 Locked",
                    font=("Segoe UI", 8),
                    bg=achievement_card["bg"],
                    fg="#999999"
                ).place(x=180, y=10)