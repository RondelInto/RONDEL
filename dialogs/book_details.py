"""Book Details Dialog Component"""
import tkinter as tk
from tkinter import scrolledtext, font as tkfont

try:
    from config import COLORS, STATUS_COLORS
except Exception:
    COLORS = {
        "background": "#f5f5f5",
        "text": "#333333",
        "primary": "#4B0082",
        "secondary": "#7A3BA3",
        "warning": "#F59E0B",
    }
    STATUS_COLORS = {
        "Reading": "#3B82F6",
        "Completed": "#10B981",
        "On Hold": "#F59E0B",
        "Not Started": "#D4B8E8",
    }

# import related dialogs via relative import (safe: __init__ doesn't import them)
try:
    from .track_progress import TrackProgressDialog
except Exception:
    TrackProgressDialog = None

try:
    from .rate_review import RateReviewDialog
except Exception:
    RateReviewDialog = None


class BookDetailsDialog:
    """Modal dialog that displays a book's details"""

    def __init__(self, parent, book, app=None):
        self.parent = parent
        self.book = book
        self.app = app

        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"Book Details — {getattr(book, 'title', 'Book')}")
        self.dialog.geometry("900x700")
        self.dialog.configure(bg=COLORS["background"])
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.focus_set()

        self._create_widgets()
        self._center()

    def _center(self):
        try:
            self.dialog.update_idletasks()
            w = self.dialog.winfo_width() or 900
            h = self.dialog.winfo_height() or 700
            x = (self.dialog.winfo_screenwidth() // 2) - (w // 2)
            y = (self.dialog.winfo_screenheight() // 2) - (h // 2)
            self.dialog.geometry(f"{w}x{h}+{x}+{y}")
        except Exception as e:
            print("center error:", e)

    def _create_widgets(self):
        container = tk.Frame(self.dialog, bg=COLORS["background"])
        container.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(container, bg=COLORS["background"], highlightthickness=0)
        vsb = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        frame = tk.Frame(canvas, bg=COLORS["background"])
        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=frame, anchor="nw")
        canvas.configure(yscrollcommand=vsb.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        self._create_header(frame)
        self._create_actions(frame)
        self._create_details(frame)

    def _create_header(self, parent):
        hf = tk.Frame(parent, bg=COLORS["background"])
        hf.pack(fill=tk.X, padx=24, pady=16)

        cover = tk.Frame(hf, bg="#f0f0f0", width=160, height=220)
        cover.pack(side=tk.LEFT)
        cover.pack_propagate(False)
        icon_font = tkfont.Font(family="Segoe UI", size=72)
        tk.Label(cover, text="📚", font=icon_font, bg="#f0f0f0").pack(expand=True)

        info = tk.Frame(hf, bg=COLORS["background"])
        info.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20)

        title_font = tkfont.Font(family="Segoe UI", size=22, weight="bold")
        tk.Label(info, text=getattr(self.book, "title", "Unknown"), font=title_font,
                 bg=COLORS["background"], fg=COLORS["primary"], wraplength=560).pack(anchor="w")

        auth_font = tkfont.Font(family="Segoe UI", size=14)
        tk.Label(info, text=f"by {getattr(self.book, 'author', 'Unknown')}", font=auth_font,
                 bg=COLORS["background"], fg="#666666").pack(anchor="w", pady=(6, 12))

        meta_frame = tk.Frame(info, bg=COLORS["background"])
        meta_frame.pack(anchor="w")
        meta_items = [
            ("Publisher", getattr(self.book, "publisher", "N/A")),
            ("Genre", getattr(self.book, "genre", "N/A")),
            ("ISBN", getattr(self.book, "isbn", "N/A")),
            ("Year", str(getattr(self.book, "year", "N/A"))),
            ("Status", getattr(self.book, "status", "N/A")),
        ]
        lab_font = tkfont.Font(family="Segoe UI", size=10, weight="bold")
        val_font = tkfont.Font(family="Segoe UI", size=10)
        row = None
        for i, (k, v) in enumerate(meta_items):
            if i % 2 == 0:
                row = tk.Frame(meta_frame, bg=COLORS["background"])
                row.pack(anchor="w", pady=4)
            # row is guaranteed to be set now
            tk.Label(row, text=f"{k}:", font=lab_font, bg=COLORS["background"], fg=COLORS["text"],
                     width=10, anchor="w").pack(side=tk.LEFT)
            tk.Label(row, text=v or "N/A", font=val_font, bg=COLORS["background"], fg="#666666",
                     width=28, anchor="w").pack(side=tk.LEFT, padx=(4, 18))

    def _create_actions(self, parent):
        af = tk.Frame(parent, bg=COLORS["background"])
        af.pack(fill=tk.X, padx=24, pady=(0, 12))
        btn_font = tkfont.Font(family="Segoe UI", size=11, weight="bold")
        tk.Button(af, text="📖 Track Reading Progress", font=btn_font,
                  bg=COLORS["primary"], fg="white", relief="flat", padx=16, pady=8,
                  command=self._open_track).pack(side=tk.LEFT, padx=(0, 8))
        tk.Button(af, text="⭐ Rate & Review", font=btn_font,
                  bg=COLORS["warning"], fg="white", relief="flat", padx=16, pady=8,
                  command=self._open_review).pack(side=tk.LEFT)

    def _create_details(self, parent):
        self._create_description(parent)
        self._create_progress(parent)
        if getattr(self.book, "rating", 0) or getattr(self.book, "review", None):
            self._create_review(parent)
        if getattr(self.book, "notes", None):
            self._create_notes(parent)
        self._create_categories(parent)

    def _create_description(self, parent):
        sf = tk.Frame(parent, bg=COLORS["background"])
        sf.pack(fill=tk.X, padx=24, pady=(8, 16))
        title_f = tkfont.Font(family="Segoe UI", size=16, weight="bold")
        tk.Label(sf, text="Description", font=title_f, bg=COLORS["background"], fg=COLORS["primary"]).pack(anchor="w", pady=(0, 8))
        desc_f = tkfont.Font(family="Segoe UI", size=10)
        st = scrolledtext.ScrolledText(sf, font=desc_f, height=6, wrap=tk.WORD, bg="white", fg=COLORS["text"])
        st.pack(fill=tk.X)
        st.insert("1.0", getattr(self.book, "description", "No description available."))
        st.config(state="disabled")

    def _create_progress(self, parent):
        sf = tk.Frame(parent, bg=COLORS["background"])
        sf.pack(fill=tk.X, padx=24, pady=(0, 16))
        title_f = tkfont.Font(family="Segoe UI", size=16, weight="bold")
        tk.Label(sf, text="Reading Progress", font=title_f, bg=COLORS["background"], fg=COLORS["primary"]).pack(anchor="w", pady=(0, 8))

        pc = tk.Frame(sf, bg="white", relief="solid", borderwidth=1, height=28)
        pc.pack(fill=tk.X, pady=6)
        pc.pack_propagate(False)
        prog = int(getattr(self.book, "progress", 0) or 0)
        prog = max(0, min(100, prog))
        bar = tk.Frame(pc, bg=STATUS_COLORS.get(getattr(self.book, "status", ""), COLORS["primary"]), height=28)
        bar.place(relwidth=prog / 100.0, relheight=1, x=0, y=0)
        lab_f = tkfont.Font(family="Segoe UI", size=10, weight="bold")
        tk.Label(pc, text=f"{prog}%", font=lab_f, bg=pc.cget("bg"), fg=COLORS["text"]).place(relx=0.5, rely=0.5, anchor="center")

        info = tk.Frame(sf, bg=COLORS["background"])
        info.pack(anchor="w", pady=(6, 0))
        if getattr(self.book, "total_pages", 0):
            tk.Label(info, text=f"Pages: {getattr(self.book, 'current_page', 0)} / {getattr(self.book, 'total_pages', 0)}",
                     font=tkfont.Font(family="Segoe UI", size=10), bg=COLORS["background"], fg="#666666").pack(side=tk.LEFT)

    def _create_review(self, parent):
        sf = tk.Frame(parent, bg=COLORS["background"])
        sf.pack(fill=tk.X, padx=24, pady=(0, 16))
        title_f = tkfont.Font(family="Segoe UI", size=16, weight="bold")
        tk.Label(sf, text="Your Review", font=title_f, bg=COLORS["background"], fg=COLORS["primary"]).pack(anchor="w", pady=(0, 8))

        rating = getattr(self.book, "rating", 0) or 0
        if rating:
            stars = "★" * int(rating) + "☆" * (5 - int(rating))
            tk.Label(sf, text=stars, font=tkfont.Font(family="Segoe UI", size=20), bg=COLORS["background"], fg=COLORS["warning"]).pack(anchor="w")
            tk.Label(sf, text=f"({rating:.1f}/5.0)", font=tkfont.Font(family="Segoe UI", size=12), bg=COLORS["background"], fg=COLORS["text"]).pack(anchor="w")

        if getattr(self.book, "review", None):
            rt = scrolledtext.ScrolledText(sf, font=tkfont.Font(family="Segoe UI", size=10), height=4, bg="white", fg=COLORS["text"])
            rt.pack(fill=tk.X)
            rt.insert("1.0", getattr(self.book, "review", ""))
            rt.config(state="disabled")

    def _create_notes(self, parent):
        sf = tk.Frame(parent, bg=COLORS["background"])
        sf.pack(fill=tk.X, padx=24, pady=(0, 16))
        tk.Label(sf, text="Your Notes", font=tkfont.Font(family="Segoe UI", size=16, weight="bold"), bg=COLORS["background"], fg=COLORS["primary"]).pack(anchor="w", pady=(0, 8))
        nt = scrolledtext.ScrolledText(sf, font=tkfont.Font(family="Segoe UI", size=10), height=4, bg="white", fg=COLORS["text"])
        nt.pack(fill=tk.X)
        nt.insert("1.0", getattr(self.book, "notes", ""))
        nt.config(state="disabled")

    def _create_categories(self, parent):
        sf = tk.Frame(parent, bg=COLORS["background"])
        sf.pack(fill=tk.X, padx=24, pady=(0, 16))
        tk.Label(sf, text="Categories", font=tkfont.Font(family="Segoe UI", size=16, weight="bold"), bg=COLORS["background"], fg=COLORS["primary"]).pack(anchor="w", pady=(0, 8))
        cf = tk.Frame(sf, bg=COLORS["background"])
        cf.pack(anchor="w")
        categories = getattr(self.book, "categories", None)
        svc = getattr(self.app, "category_service", None) if self.app is not None else None
        if categories and svc:
            for n in categories:
                try:
                    cat = svc.get_category_by_name(n)
                    if cat:
                        tk.Label(cf, text=getattr(cat, "name", n), font=tkfont.Font(family="Segoe UI", size=9, weight="bold"),
                                 bg=getattr(cat, "color", "#4B0082"), fg="white", padx=10, pady=3).pack(side=tk.LEFT, padx=(0, 8), pady=4)
                except Exception as e:
                    print("category badge error:", e)
        else:
            tk.Label(cf, text="No categories assigned", font=tkfont.Font(family="Segoe UI", size=10), bg=COLORS["background"], fg="#999999").pack(anchor="w")
    # actions
    def _open_track(self):
        if TrackProgressDialog:
            self.dialog.destroy()
            TrackProgressDialog(self.parent, self.book, self.app)
        else:
            print("TrackProgressDialog unavailable")

    def _open_review(self):
        if RateReviewDialog:
            self.dialog.destroy()
            RateReviewDialog(self.parent, self.book, self.app)
        else:
            print("RateReviewDialog unavailable")