"""Libris Core - Library Management System"""
import os
import sys
import re
import importlib
import inspect
import types
import tkinter as tk
from tkinter import ttk, messagebox

# Basic typing
from typing import Optional, Protocol

class Refreshable(Protocol):
    def refresh(self) -> None: ...
# Adjust path for imports (helps with module resolution)
root_dir = os.path.dirname(os.path.abspath(__file__))
# ensure project root is on sys.path and avoid duplicates
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# Config/colors
try:
    from config import COLORS
except Exception as e:
    print(f"Warning: cannot import config.COLORS: {e}")
    COLORS = {
        "background": "#f5f6fa",
        "primary": "#4B0082",
        "secondary": "#6A0DAD",
        "text": "#222222",
        "light": "#bfbfbf",
        "success": "#28a745",
        "danger": "#dc3545"
    }

# helper: CamelCase -> snake_case
def camel_to_snake(name: str) -> str:
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def discover_classes_in_package(pkg: str, wanted: list[str]) -> dict[str, Optional[type]]:
    """Import modules in package and return mapping class_name -> class object for classes in wanted.
    Behavior:
      - Try to import the package and use its __path__ if available
      - Fall back to a filesystem path relative to this file
      - Reload modules already in sys.modules to pick up changes
      - Log and skip modules that fail to import
    """
    found = {name: None for name in wanted}
    try:
        pkg_paths = []
        # Prefer importing the package to get a reliable __path__
        try:
            pkg_mod = importlib.import_module(pkg)
            pkg_paths = list(getattr(pkg_mod, "__path__", []))
        except Exception:
            pkg_paths = []

        # Fallback to filesystem relative to this file
        if not pkg_paths:
            pkg_fs = os.path.join(os.path.dirname(__file__), pkg.replace(".", os.sep))
            if os.path.isdir(pkg_fs):
                pkg_paths = [pkg_fs]

        if not pkg_paths:
            return found

        for base in pkg_paths:
            for fname in sorted(os.listdir(base)):
                if not fname.endswith(".py") or fname.startswith("__"):
                    continue
                mod_name = fname[:-3]
                full_mod = f"{pkg}.{mod_name}"
                try:
                    if full_mod in sys.modules:
                        mod = importlib.reload(sys.modules[full_mod])
                    else:
                        mod = importlib.import_module(full_mod)
                except Exception as ie:
                    # don't fail the whole discovery if one module breaks
                    print(f"Skipping module {full_mod}: {ie}")
                    continue
                for cls_name, cls_obj in inspect.getmembers(mod, inspect.isclass):
                    if cls_name in wanted:
                        found[cls_name] = cls_obj
    except Exception as e:
        print(f"discover_classes_in_package error for {pkg}: {e}")
    return found

# discover components and admin classes
component_class_names = ['Header', 'LibraryTab', 'StatsTab', 'CategoriesTab', 'AddBookTab', 'SearchTab']
components_imports = discover_classes_in_package('components', component_class_names)

admin_class_names = ['AdminDashboard']
admin_imports = discover_classes_in_package('components.admin', admin_class_names)

# services: expected service class names in files
service_class_names = ['BookService', 'CategoryService', 'StatsService', 'AchievementService']
services_imports = discover_classes_in_package('services', service_class_names)

# Provide a holder in case services package is imported elsewhere.
# If services package isn't present, create a proper ModuleType with a __path__.
try:
    import services as services_pkg
except Exception:
    services_pkg = types.ModuleType("services")
    services_dir = os.path.join(os.path.dirname(__file__), "services")
    if os.path.isdir(services_dir):
        # set package __path__ so pkgutil/import mechanisms treat it as a package
        services_pkg.__path__ = [services_dir]
    else:
        # empty path still signals a package object for attribute export
        services_pkg.__path__ = []
    sys.modules["services"] = services_pkg

class LoginUI:
    def __init__(self, parent, on_login_callback):
        self.parent = parent
        self.on_login_callback = on_login_callback
        self.frame = tk.Frame(parent, bg=COLORS["background"])
        self._build()

    def _build(self):
        tk.Label(self.frame, text="Libris Core — Login", font=("Segoe UI", 18, "bold"),
                 bg=COLORS["background"], fg=COLORS["primary"]).pack(pady=20)
        frm = tk.Frame(self.frame, bg=COLORS["background"])
        frm.pack(pady=10, padx=20)

        tk.Label(frm, text="Username:", bg=COLORS["background"]).grid(row=0, column=0, sticky="w")
        self.username = tk.Entry(frm)
        self.username.grid(row=0, column=1, padx=8, pady=6)

        tk.Label(frm, text="Password:", bg=COLORS["background"]).grid(row=1, column=0, sticky="w")
        self.password = tk.Entry(frm, show="*")
        self.password.grid(row=1, column=1, padx=8, pady=6)

        self.account_type_var = tk.StringVar(value="User")
        tk.OptionMenu(frm, self.account_type_var, "User", "Admin").grid(row=2, column=1, sticky="w", pady=6)

        tk.Button(self.frame, text="Sign In", bg=COLORS["primary"], fg="white",
                  command=self._on_signin_click).pack(pady=12)

    def _on_signin_click(self):
        username = self.username.get().strip()
        password = self.password.get().strip()
        # Basic local credential check (placeholder)
        valid_users = {
            "user": {"password": "user123", "type": "User"},
            "admin": {"password": "admin123", "type": "Admin"}
        }
        if username in valid_users and valid_users[username]["password"] == password:
            real_type = valid_users[username]["type"]
            self.on_login_callback(username, real_type)
        else:
            messagebox.showerror("Login failed", "Invalid credentials")

class LibraryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Libris Core")
        self.root.configure(bg=COLORS["background"])
        self.services = {}
        self._instantiate_services()
        self._export_services()
        self.content_frame = None
        self.header = None
        self.current_tab = None
        self.tabs = {}
        self._create_login_interface()

    def _instantiate_services(self):
        # Instantiate service classes discovered earlier and store instances in self.services
        for svc_name, svc_cls in services_imports.items():
            if svc_cls:
                try:
                    inst = svc_cls()
                except Exception as e:
                    print(f"Failed to instantiate {svc_name}: {e}")
                    inst = None
                self.services[svc_name] = inst
            else:
                self.services[svc_name] = None

    def _export_services(self):
        # make single instances available as attributes on services package
        try:
            import services as services_pkg
            setattr(services_pkg, "book_service", self.services.get("BookService"))
            setattr(services_pkg, "category_service", self.services.get("CategoryService"))
            setattr(services_pkg, "stats_service", self.services.get("StatsService"))
            # optional achievement service
            setattr(services_pkg, "achievement_service", self.services.get("AchievementService"))
        except Exception as e:
            print(f"Warning exporting services to services package: {e}")

        # also provide direct attributes on app for convenience
        self.book_service = self.services.get("BookService")
        self.category_service = self.services.get("CategoryService")
        self.stats_service = self.services.get("StatsService")
        self.achievement_service = self.services.get("AchievementService")

    def _create_login_interface(self):
        # Clear root
        for w in self.root.winfo_children():
            w.destroy()
        self.login_ui = LoginUI(self.root, self._on_login_success)
        self.login_ui.frame.pack(fill=tk.BOTH, expand=True)

    def _on_login_success(self, username, account_type):
        self.current_user = username
        self.account_type = account_type
        # Create main layout
        for w in self.root.winfo_children():
            w.destroy()
        # Header (optional if provided in components)
        header_cls = components_imports.get('Header')
        if header_cls:
            try:
                self.header = header_cls(self.root, self)
                if hasattr(self.header, 'frame'):
                    self.header.frame.pack(fill=tk.X)
            except Exception as e:
                print(f"Header instantiate error: {e}")
        # content area
        self.create_content_area()
        # load admin or user interface
        if account_type == "Admin" and admin_imports.get("AdminDashboard"):
            try:
                admin_cls = admin_imports["AdminDashboard"]
                self.admin_dashboard = admin_cls(self.content_frame, self)
                if hasattr(self.admin_dashboard, "frame"):
                    self.admin_dashboard.frame.pack(fill=tk.BOTH, expand=True)
            except Exception as e:
                print(f"AdminDashboard error: {e}")
        else:
            # user default to library tab
            self.show_library()

    def create_content_area(self):
        if self.content_frame:
            self.content_frame.destroy()
        self.content_frame = tk.Frame(self.root, bg=COLORS["background"])
        self.content_frame.pack(fill=tk.BOTH, expand=True)

    def _switch_to_tab(self, tab_name):
        # hide current
        if self.current_tab and hasattr(self.current_tab, "frame"):
            self.current_tab.frame.pack_forget()
        # instantiate if needed
        if tab_name not in self.tabs:
            cls = components_imports.get(tab_name)
            if not cls:
                print(f"Component {tab_name} not available")
                return
            try:
                inst = cls(self.content_frame, self)
                self.tabs[tab_name] = inst
            except Exception as e:
                print(f"Error creating {tab_name}: {e}")
                return
        self.current_tab = self.tabs[tab_name]
        if hasattr(self.current_tab, "frame"):
            self.current_tab.frame.pack(fill=tk.BOTH, expand=True)

    def show_library(self):
        self._switch_to_tab('LibraryTab')

    def show_stats(self):
        self._switch_to_tab('StatsTab')

    def show_categories(self):
        self._switch_to_tab('CategoriesTab')

    def show_add_book(self):
        self._switch_to_tab('AddBookTab')

    def show_search(self):
        self._switch_to_tab('SearchTab')

    def refresh_all(self):
        # call refresh on known refreshable components
        for inst in self.tabs.values():
            if hasattr(inst, "refresh"):
                try:
                    inst.refresh()
                except Exception:
                    pass
        # admin dashboard refresh
        if hasattr(self, "admin_dashboard") and getattr(self.admin_dashboard, "refresh", None):
            try:
                self.admin_dashboard.refresh()
            except Exception:
                pass


if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryManagementSystem(root)
    # center window
    try:
        root.geometry("1000x700")
        root.update_idletasks()
        w = root.winfo_width()
        h = root.winfo_height()
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        x = (sw // 2) - (w // 2)
        y = (sh // 2) - (h // 2)
        root.geometry(f"+{x}+{y}")
    except Exception:
        pass
    root.mainloop()
