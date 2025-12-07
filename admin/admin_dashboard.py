"""Main Admin Dashboard Component"""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import sqlite3
import csv
import os
from datetime import datetime
from typing import Optional, cast, Dict

class AdminDashboard:
    """
    Main Admin Dashboard component.
    Usage: AdminDashboard(parent_frame, app, book_service=..., category_service=..., stats_service=..., db_connection=...)
    """
    def __init__(self, parent, app=None, book_service=None, category_service=None, stats_service=None, db_connection=None):
        self.parent = parent
        self.app = app
        self.book_service = book_service or getattr(app, "book_service", None)
        self.category_service = category_service or getattr(app, "category_service", None)
        self.stats_service = stats_service or getattr(app, "stats_service", None)

        # establish a concrete sqlite3.Connection (avoid Optional for type-checker)
        conn_val = db_connection or getattr(app, "db_connection", None)
        if conn_val is None:
            db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "libris_core.db")
            try:
                conn_val = sqlite3.connect(db_path)
                conn_val.row_factory = sqlite3.Row
            except Exception:
                conn_val = sqlite3.connect(":memory:")
                conn_val.row_factory = sqlite3.Row

        # tell the type-checker this is a real Connection
        self.conn: sqlite3.Connection = cast(sqlite3.Connection, conn_val)

        # ensure minimal schema so queries don't fail
        try:
            self._ensure_schema()
        except Exception:
            pass

        # theme (can be overridden on app)
        self.colors = getattr(app, "colors", {
            'primary': '#4B0082', 'primary_light': '#7A3BA3',
            'primary_dark': '#3A0066', 'background': '#F2F2F2',
            'text_primary': '#1A1A1A'
        })

        # UI placeholders with explicit Optional typing
        self.content_frame: Optional[tk.Frame] = None
        self.books_tree: Optional[ttk.Treeview] = None
        self.users_tree: Optional[ttk.Treeview] = None
        self.transactions_tree: Optional[ttk.Treeview] = None
        self.books_context_menu: Optional[tk.Menu] = None

        # declare policy_entries so type-checker/Pylance knows it's a dict of Entry widgets
        self.policy_entries: Dict[str, tk.Entry] = {}

        # Build UI and default view
        self._build_ui()
        self.show_admin_dashboard_content()

    def build_or_refresh(self):
        """Call when parent changed or when you want to rebuild the UI."""
        self._build_ui()
        self.show_admin_dashboard_content()

    def _build_ui(self):
        # clear parent
        for w in self.parent.winfo_children():
            w.destroy()

        header = tk.Frame(self.parent, bg=self.colors['primary'], height=64)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        tk.Label(header, text="LIBRIS CORE — Admin", fg="white", bg=self.colors['primary'],
                 font=("Segoe UI", 14, "bold")).pack(side=tk.LEFT, padx=12, pady=10)
        logout_btn = tk.Button(header, text="Logout", command=self._on_logout)
        logout_btn.pack(side=tk.RIGHT, padx=12, pady=10)

        main = tk.Frame(self.parent, bg=self.colors['background'])
        main.pack(fill=tk.BOTH, expand=True)

        sidebar = tk.Frame(main, bg=self.colors['primary_dark'], width=200)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        menu = [
            ("Dashboard", self.show_admin_dashboard_content),
            ("Books", self.show_books_management),
            ("Users", self.show_users_management),
            ("Transactions", self.show_transactions),
            ("Policies", self.show_library_policies),
            ("Reports", self.generate_reports),
        ]
        for t, cmd in menu:
            b = tk.Button(sidebar, text=t, command=cmd, anchor="w")
            b.pack(fill=tk.X, padx=6, pady=4)

        self.content_frame = tk.Frame(main, bg=self.colors['background'])
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

    def _on_logout(self):
        # use getattr + callable to avoid "attribute of None" warnings from Pylance
        logout_fn = getattr(self.app, "_logout", None)
        if callable(logout_fn):
            try:
                logout_fn()
            except Exception:
                pass
        else:
            self.parent.winfo_toplevel().destroy()

    def show_admin_dashboard_content(self):
        # help type checker: self.content_frame must be present
        assert self.content_frame is not None
        self._clear_content()
        tk.Label(self.content_frame, text="Admin Dashboard", font=("Segoe UI", 16, "bold"),
                 bg=self.colors['background']).pack(anchor="w")

        total_books = 0
        total_users = 0
        try:
            if self.stats_service and hasattr(self.stats_service, "get_counts"):
                stats = self.stats_service.get_counts()
                total_books = stats.get("books", 0)
                total_users = stats.get("users", 0)
            else:
                cur = self.conn.cursor()
                cur.execute("SELECT COUNT(*) FROM books")
                total_books = cur.fetchone()[0]
                cur.execute("SELECT COUNT(*) FROM users")
                total_users = cur.fetchone()[0]
        except Exception:
            pass

        sframe = tk.Frame(self.content_frame, bg=self.colors['background'])
        sframe.pack(fill=tk.X, pady=8)
        tk.Label(sframe, text=f"Total Books: {total_books}", bg=self.colors['background']).pack(side=tk.LEFT, padx=6)
        tk.Label(sframe, text=f"Total Users: {total_users}", bg=self.colors['background']).pack(side=tk.LEFT, padx=6)

    def show_books_management(self):
        assert self.content_frame is not None
        self._clear_content()
        header = tk.Frame(self.content_frame, bg=self.colors['background'])
        header.pack(fill=tk.X)
        tk.Button(header, text="+ Add New Book", command=self._add_book_handler).pack(side=tk.LEFT, padx=6)
        tk.Button(header, text="Import CSV", command=self._import_books_csv).pack(side=tk.LEFT, padx=6)
        tk.Button(header, text="Export CSV", command=self._export_books_csv).pack(side=tk.LEFT, padx=6)

        table_frame = tk.Frame(self.content_frame, bg=self.colors['background'])
        table_frame.pack(fill=tk.BOTH, expand=True)

        cols = ('ID','Title','Author','ISBN','Genre','Quantity','Available','Publisher','Year')
        self.books_tree = ttk.Treeview(table_frame, columns=cols, show='headings', height=12)
        for c in cols:
            self.books_tree.heading(c, text=c)
            self.books_tree.column(c, width=100)
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.books_tree.yview)
        self.books_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.books_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.books_tree.bind("<Button-3>", self._on_books_context_menu)

        # context menu
        self.books_context_menu = tk.Menu(self.parent, tearoff=0)
        self.books_context_menu.add_command(label="Edit Book", command=self._edit_selected_book)
        self.books_context_menu.add_command(label="Delete Book", command=self._delete_selected_book)

        self._refresh_books_table()

    def _refresh_books_table(self):
        if self.books_tree is None:
            return
        for i in self.books_tree.get_children():
            self.books_tree.delete(i)

        try:
            if self.book_service and hasattr(self.book_service, "list_books"):
                books = self.book_service.list_books()
                for b in books:
                    vals = (
                        getattr(b, "id", None) or b.get("id", ""),
                        getattr(b, "title", None) or b.get("title", ""),
                        getattr(b, "author", None) or b.get("author", ""),
                        getattr(b, "isbn", None) or b.get("isbn", ""),
                        getattr(b, "genre", None) or b.get("genre", ""),
                        getattr(b, "quantity", None) or b.get("quantity", ""),
                        getattr(b, "available", None) or b.get("available", ""),
                        getattr(b, "publisher", None) or b.get("publisher", ""),
                        getattr(b, "publication_year", None) or b.get("publication_year", ""),
                    )
                    self.books_tree.insert('', tk.END, values=vals)
            else:
                cur = self.conn.cursor()
                cur.execute('SELECT id, title, author, isbn, genre, quantity, available, publisher, publication_year FROM books')
                for row in cur.fetchall():
                    self.books_tree.insert('', tk.END, values=row)
        except Exception:
            pass

    def _add_book_handler(self):
        dialog = tk.Toplevel(self.parent); dialog.title("Add Book")
        frame = tk.Frame(dialog, padx=12, pady=12); frame.pack()
        entries = {}
        fields = [("Title",""),("Author",""),("ISBN",""),("Genre",""),("Publisher",""),("Year",""),("Quantity","1")]
        for i,(label,defv) in enumerate(fields):
            tk.Label(frame, text=label).grid(row=i,column=0,sticky='w')
            e = tk.Entry(frame); e.grid(row=i,column=1)
            e.insert(0,str(defv)); entries[label]=e

        def save():
            data = {
                "title": entries["Title"].get(),
                "author": entries["Author"].get(),
                "isbn": entries["ISBN"].get(),
                "genre": entries["Genre"].get(),
                "publisher": entries["Publisher"].get(),
                "publication_year": entries["Year"].get(),
                "quantity": int(entries["Quantity"].get() or 1),
                "available": int(entries["Quantity"].get() or 1)
            }
            try:
                if self.book_service and hasattr(self.book_service, "create_book"):
                    self.book_service.create_book(data)
                else:
                    cur = self.conn.cursor()
                    cur.execute('''
                        INSERT INTO books (title, author, isbn, genre, publisher, publication_year, quantity, available, created_date)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (data["title"], data["author"], data["isbn"], data["genre"], data["publisher"],
                          data["publication_year"], data["quantity"], data["available"], datetime.now().strftime("%Y-%m-%d")))
                    # guard commit with conn check for type-checker
                    if self.conn is not None:
                        self.conn.commit()
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                dialog.destroy()
                self._refresh_books_table()

        tk.Button(frame, text="Save", command=save).grid(row=len(fields), column=0, pady=8)
        tk.Button(frame, text="Cancel", command=dialog.destroy).grid(row=len(fields), column=1, pady=8)

    def _edit_selected_book(self):
        # ensure tree exists
        assert self.books_tree is not None
        sel = self.books_tree.selection()
        if not sel:
            return
        vals = self.books_tree.item(sel[0])['values']
        if not vals:
            return
        book_id = vals[0]

        # Treeview values may be strings/Any — ensure initialvalue is int or None
        raw_init = vals[5] if len(vals) > 5 else None
        try:
            initial_val = int(raw_init) if raw_init not in (None, "") else 1
        except (ValueError, TypeError):
            initial_val = 1
        new_q = simpledialog.askinteger("Update Quantity", "New total quantity:", initialvalue=initial_val)

        if new_q is None:
            return
        try:
            if self.book_service and hasattr(self.book_service, "update_book"):
                self.book_service.update_book(book_id, {"quantity": new_q})
            else:
                cur = self.conn.cursor()
                cur.execute('UPDATE books SET quantity = ? WHERE id = ?', (new_q, book_id))
                if self.conn is not None:
                    self.conn.commit()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            self._refresh_books_table()

    def _delete_selected_book(self):
        assert self.books_tree is not None
        sel = self.books_tree.selection()
        if not sel: return
        vals = self.books_tree.item(sel[0])['values']
        book_id = vals[0]
        if not messagebox.askyesno("Confirm", "Delete this book?"): return
        try:
            if self.book_service and hasattr(self.book_service, "delete_book"):
                self.book_service.delete_book(book_id)
            else:
                cur = self.conn.cursor()
                cur.execute('DELETE FROM books WHERE id = ?', (book_id,))
                if self.conn is not None:
                    self.conn.commit()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            self._refresh_books_table()

    # minimal implementations for other menu items to avoid runtime errors
    def show_users_management(self):
        assert self.content_frame is not None
        self._clear_content()
        tk.Label(self.content_frame, text="Users Management", font=("Segoe UI", 14)).pack(anchor="w")
        # simple users table
        self.users_tree = ttk.Treeview(self.content_frame, columns=('ID','Username','Name','Email','Type','Status'), show='headings')
        for c in ('ID','Username','Name','Email','Type','Status'):
            self.users_tree.heading(c, text=c)
        self.users_tree.pack(fill=tk.BOTH, expand=True)
        # fill
        try:
            cur = self.conn.cursor()
            cur.execute('SELECT id, username, name, email, user_type, status FROM users')
            for row in cur.fetchall():
                self.users_tree.insert('', tk.END, values=row)
        except Exception:
            pass

    def show_transactions(self):
        assert self.content_frame is not None
        self._clear_content()
        tk.Label(self.content_frame, text="Transactions", font=("Segoe UI", 14)).pack(anchor="w")
        self.transactions_tree = ttk.Treeview(self.content_frame, columns=('ID','User','Book','Borrow Date','Due Date','Return Date','Status','Fine'), show='headings')
        for c in ('ID','User','Book','Borrow Date','Due Date','Return Date','Status','Fine'):
            self.transactions_tree.heading(c, text=c)
        self.transactions_tree.pack(fill=tk.BOTH, expand=True)
        try:
            cur = self.conn.cursor()
            cur.execute('SELECT t.id, u.name, b.title, t.borrow_date, t.due_date, t.return_date, t.status, t.fine_amount FROM transactions t JOIN users u ON t.user_id = u.id JOIN books b ON t.book_id = b.id ORDER BY t.borrow_date DESC')
            for row in cur.fetchall():
                self.transactions_tree.insert('', tk.END, values=row)
        except Exception:
            pass

    def show_library_policies(self):
        assert self.content_frame is not None
        self._clear_content()
        tk.Label(self.content_frame, text="Library Policies", font=("Segoe UI", 14)).pack(anchor="w")
        self.policy_entries = {}
        row = tk.Frame(self.content_frame); row.pack(fill=tk.X, pady=6)
        tk.Label(row, text="Borrow Period (days)").pack(side=tk.LEFT)
        e = tk.Entry(row); e.pack(side=tk.RIGHT); self.policy_entries["borrow_period"] = e
        tk.Button(self.content_frame, text="Save Policies", command=self._save_policies).pack(pady=8)

    def _save_policies(self):
        try:
            entry = self.policy_entries.get("borrow_period")
            raw = entry.get() if entry is not None else ""
            try:
                val = int(raw) if raw not in ("", None) else 28
            except (ValueError, TypeError):
                val = 28
            cur = self.conn.cursor()
            cur.execute('INSERT OR REPLACE INTO policies (id, borrow_period_days) VALUES (1, ?)', (val,))
            self.conn.commit()
            messagebox.showinfo("Saved", "Policies saved")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def generate_reports(self):
        messagebox.showinfo("Reports", "Use the UI to export reports (books/users/transactions).")

    def _import_books_csv(self):
        filename = filedialog.askopenfilename(filetypes=[("CSV","*.csv")])
        if not filename: return
        try:
            with open(filename, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                cur = self.conn.cursor()
                for r in reader:
                    cur.execute('''
                        INSERT OR IGNORE INTO books (title, author, isbn, genre, publisher, publication_year, quantity, available, created_date)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (r.get('title',''), r.get('author',''), r.get('isbn',''), r.get('genre',''),
                          r.get('publisher',''), r.get('publication_year'), int(r.get('quantity') or 1),
                          int(r.get('quantity') or 1), datetime.now().strftime('%Y-%m-%d')))
                if self.conn is not None:
                    self.conn.commit()
            messagebox.showinfo("Import", "Import completed")
        except Exception as e:
            messagebox.showerror("Import Error", str(e))
        finally:
            self._refresh_books_table()

    def _export_books_csv(self):
        filename = filedialog.asksaveasfilename(defaultextension=".csv")
        if not filename: return
        try:
            cur = self.conn.cursor()
            cur.execute('SELECT title,author,isbn,genre,publisher,publication_year,quantity,available FROM books')
            rows = cur.fetchall()
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                w = csv.writer(f); w.writerow(['title','author','isbn','genre','publisher','year','quantity','available']); w.writerows(rows)
            messagebox.showinfo("Export", "Export completed")
        except Exception as e:
            messagebox.showerror("Export Error", str(e))

    # utilities
    def _clear_content(self):
        if self.content_frame:
            for w in self.content_frame.winfo_children():
                w.destroy()

    def _on_books_context_menu(self, event):
        if not self.books_tree: return
        item = self.books_tree.identify_row(event.y)
        if item:
            self.books_tree.selection_set(item)
            try:
                if self.books_context_menu:
                    self.books_context_menu.post(event.x_root, event.y_root)
            except Exception:
                pass

    def _ensure_schema(self):
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT, author TEXT, isbn TEXT, genre TEXT,
                publisher TEXT, publication_year TEXT,
                quantity INTEGER DEFAULT 0, available INTEGER DEFAULT 0,
                created_date TEXT
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT, name TEXT, email TEXT,
                user_type TEXT, status TEXT, join_date TEXT, borrowed_count INTEGER DEFAULT 0
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER, book_id INTEGER,
                borrow_date TEXT, due_date TEXT, return_date TEXT,
                status TEXT, fine_amount REAL DEFAULT 0
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS policies (
                id INTEGER PRIMARY KEY,
                borrow_period_days INTEGER DEFAULT 28,
                max_books_per_user INTEGER DEFAULT 5,
                fine_per_day REAL DEFAULT 0.5
            )
        """)
        if self.conn is not None:
            self.conn.commit()
# end AdminDashboard