import tkinter as tk

from config.settings import WINDOW_TITLE, DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT
from core.app_state import AppState
from gui.theme_manager import ThemeManager
from gui.pages.dashboard_page import DashboardPage
from gui.pages.git_page import GitPage


class GHWorkspaceApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.app_state = AppState()
        self.theme_manager = ThemeManager(self.app_state)

        width = self.app_state.config_manager.get("window_width", DEFAULT_WINDOW_WIDTH)
        height = self.app_state.config_manager.get("window_height", DEFAULT_WINDOW_HEIGHT)

        self.title(WINDOW_TITLE)
        self.geometry(f"{width}x{height}")

        self.sidebar = tk.Frame(self, width=200)
        self.sidebar.pack(side="left", fill="y")

        self.content = tk.Frame(self)
        self.content.pack(side="right", expand=True, fill="both")

        self.pages = {}

        self.create_sidebar()
        self.create_pages()
        self.apply_theme()
        self.show_page(self.app_state.current_page)

    def create_sidebar(self):
        self.sidebar_title = tk.Label(
            self.sidebar,
            text="GH Workspace",
            font=("Arial", 14, "bold")
        )
        self.sidebar_title.pack(pady=20)

        self.dashboard_button = tk.Button(
            self.sidebar,
            text="Dashboard",
            width=20,
            command=lambda: self.show_page("dashboard")
        )
        self.dashboard_button.pack(pady=5)

        self.git_button = tk.Button(
            self.sidebar,
            text="Git Manager",
            width=20,
            command=lambda: self.show_page("git")
        )
        self.git_button.pack(pady=5)

        self.theme_button = tk.Button(
            self.sidebar,
            text="Toggle Theme",
            width=20,
            command=self.toggle_theme
        )
        self.theme_button.pack(pady=25)

    def create_pages(self):
        self.pages["dashboard"] = DashboardPage(self.content, self.app_state)
        self.pages["git"] = GitPage(self.content, self.app_state)

        for page in self.pages.values():
            page.place(relwidth=1, relheight=1)

    def show_page(self, name):
        if name not in self.pages:
            name = "dashboard"

        self.app_state.set_current_page(name)
        self.pages[name].tkraise()

    def toggle_theme(self):
        current_theme = self.theme_manager.get_theme_name()
        new_theme = "dark" if current_theme == "light" else "light"
        self.theme_manager.set_theme_name(new_theme)
        self.apply_theme()

    def apply_theme(self):
        theme = self.theme_manager.get_theme()

        self.configure(bg=theme["bg"])
        self.sidebar.configure(bg=theme["sidebar_bg"])
        self.content.configure(bg=theme["content_bg"])

        self.sidebar_title.configure(
            bg=theme["sidebar_bg"],
            fg=theme["fg"]
        )

        for button in [
            self.dashboard_button,
            self.git_button,
            self.theme_button
        ]:
            button.configure(
                bg=theme["button_bg"],
                fg=theme["button_fg"],
                activebackground=theme["content_bg"],
                activeforeground=theme["fg"]
            )

        for page in self.pages.values():
            if hasattr(page, "apply_theme"):
                page.apply_theme(theme)
