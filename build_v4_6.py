from pathlib import Path

files = {
    "src/config/settings.py": '''APP_NAME = "GH Workspace Manager"
APP_VERSION = "4.6"
WINDOW_TITLE = f"{APP_NAME} V{APP_VERSION}"

DEFAULT_WINDOW_WIDTH = 1100
DEFAULT_WINDOW_HEIGHT = 700

CONFIG_FILE_NAME = "gh_workspace_config.json"
LOG_FILE_NAME = "gh_workspace.log"
DEFAULT_THEME = "light"
''',

    "src/gui/theme_manager.py": '''class ThemeManager:
    THEMES = {
        "light": {
            "bg": "#f4f4f4",
            "fg": "#111111",
            "sidebar_bg": "#dddddd",
            "button_bg": "#eeeeee",
            "button_fg": "#111111",
            "content_bg": "#ffffff",
            "text_bg": "#ffffff",
            "text_fg": "#111111"
        },
        "dark": {
            "bg": "#1e1e1e",
            "fg": "#f5f5f5",
            "sidebar_bg": "#2b2b2b",
            "button_bg": "#3a3a3a",
            "button_fg": "#ffffff",
            "content_bg": "#252525",
            "text_bg": "#111111",
            "text_fg": "#ffffff"
        }
    }

    def __init__(self, app_state):
        self.app_state = app_state

    def get_theme_name(self):
        return self.app_state.config_manager.get("theme", "light")

    def set_theme_name(self, theme_name):
        if theme_name not in self.THEMES:
            theme_name = "light"

        self.app_state.config_manager.set("theme", theme_name)
        self.app_state.logger.info(f"Theme changed to: {theme_name}")

    def get_theme(self):
        return self.THEMES.get(self.get_theme_name(), self.THEMES["light"])
''',

    "src/gui/app.py": '''import tkinter as tk

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
''',

    "src/gui/pages/dashboard_page.py": '''import tkinter as tk
from core.paths import APP_LOG_FILE


class DashboardPage(tk.Frame):
    def __init__(self, parent, app_state):
        super().__init__(parent)
        self.app_state = app_state

        self.title = tk.Label(
            self,
            text="Dashboard & Workspace Health",
            font=("Arial", 18, "bold")
        )
        self.title.pack(pady=20)

        self.message = tk.Label(
            self,
            text="GH Workspace Manager professional modular architecture is running.",
            font=("Arial", 12)
        )
        self.message.pack(pady=10)

        self.log_info = tk.Label(
            self,
            text=f"Log file: {APP_LOG_FILE}",
            font=("Arial", 10)
        )
        self.log_info.pack(pady=10)

    def apply_theme(self, theme):
        self.configure(bg=theme["content_bg"])
        self.title.configure(bg=theme["content_bg"], fg=theme["fg"])
        self.message.configure(bg=theme["content_bg"], fg=theme["fg"])
        self.log_info.configure(bg=theme["content_bg"], fg=theme["fg"])
''',

    "src/gui/pages/git_page.py": '''import tkinter as tk
from services.git_service import GitService
from core.paths import PROJECT_ROOT


class GitPage(tk.Frame):
    def __init__(self, parent, app_state):
        super().__init__(parent)
        self.app_state = app_state
        self.git_service = GitService(PROJECT_ROOT)

        self.title = tk.Label(self, text="Git Manager", font=("Arial", 18, "bold"))
        self.title.pack(pady=20)

        self.status_button = tk.Button(self, text="Show Git Status", command=self.show_status)
        self.status_button.pack(pady=5)

        self.log_button = tk.Button(self, text="Show Recent Commits", command=self.show_log)
        self.log_button.pack(pady=5)

        self.output = tk.Text(self, height=20, width=100)
        self.output.pack(pady=10)

    def show_status(self):
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, self.git_service.status())

    def show_log(self):
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, self.git_service.log())

    def apply_theme(self, theme):
        self.configure(bg=theme["content_bg"])
        self.title.configure(bg=theme["content_bg"], fg=theme["fg"])

        for button in [self.status_button, self.log_button]:
            button.configure(
                bg=theme["button_bg"],
                fg=theme["button_fg"],
                activebackground=theme["content_bg"],
                activeforeground=theme["fg"]
            )

        self.output.configure(
            bg=theme["text_bg"],
            fg=theme["text_fg"],
            insertbackground=theme["text_fg"]
        )
'''
}


def main():
    for path, content in files.items():
        file_path = Path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        print(f"Updated: {file_path}")

    print("\\nV4.6 Theme Manager created successfully.")


if __name__ == "__main__":
    main()
