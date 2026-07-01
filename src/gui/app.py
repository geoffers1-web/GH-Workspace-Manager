import tkinter as tk

from config.settings import WINDOW_TITLE, DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT
from core.app_state import AppState
from gui.pages.dashboard_page import DashboardPage
from gui.pages.git_page import GitPage


class GHWorkspaceApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.app_state = AppState()

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
        self.show_page(self.app_state.current_page)

    def create_sidebar(self):
        tk.Label(
            self.sidebar,
            text="GH Workspace",
            font=("Arial", 14, "bold")
        ).pack(pady=20)

        tk.Button(
            self.sidebar,
            text="Dashboard",
            width=20,
            command=lambda: self.show_page("dashboard")
        ).pack(pady=5)

        tk.Button(
            self.sidebar,
            text="Git Manager",
            width=20,
            command=lambda: self.show_page("git")
        ).pack(pady=5)

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
