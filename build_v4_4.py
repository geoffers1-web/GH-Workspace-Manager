from pathlib import Path

files = {
    "src/config/settings.py": '''APP_NAME = "GH Workspace Manager"
APP_VERSION = "4.4"
WINDOW_TITLE = f"{APP_NAME} V{APP_VERSION}"

DEFAULT_WINDOW_WIDTH = 1100
DEFAULT_WINDOW_HEIGHT = 700

CONFIG_FILE_NAME = "gh_workspace_config.json"
''',

    "src/config/config_manager.py": '''import json
from pathlib import Path


class ConfigManager:
    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.default_config = {
            "app_name": "GH Workspace Manager",
            "version": "4.4",
            "theme": "light",
            "last_page": "dashboard",
            "window_width": 1100,
            "window_height": 700
        }
        self.config = self.load_config()

    def load_config(self):
        if not self.config_path.exists():
            self.save_config(self.default_config)
            return self.default_config.copy()

        try:
            with self.config_path.open("r", encoding="utf-8") as file:
                loaded = json.load(file)

            config = self.default_config.copy()
            config.update(loaded)
            return config

        except Exception:
            self.save_config(self.default_config)
            return self.default_config.copy()

    def save_config(self, config=None):
        if config is None:
            config = self.config

        self.config_path.parent.mkdir(parents=True, exist_ok=True)

        with self.config_path.open("w", encoding="utf-8") as file:
            json.dump(config, file, indent=4)

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        self.save_config()
''',

    "src/core/paths.py": '''from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"
DOCS_DIR = PROJECT_ROOT / "docs"
CONFIG_DIR = SRC_DIR / "config"
APP_CONFIG_DIR = PROJECT_ROOT / ".gh_workspace"
APP_CONFIG_FILE = APP_CONFIG_DIR / "gh_workspace_config.json"
''',

    "src/core/app_state.py": '''from config.config_manager import ConfigManager
from core.paths import APP_CONFIG_FILE


class AppState:
    def __init__(self):
        self.config_manager = ConfigManager(APP_CONFIG_FILE)
        self.current_page = self.config_manager.get("last_page", "dashboard")
        self.status_message = "Ready"

    def set_current_page(self, page_name):
        self.current_page = page_name
        self.config_manager.set("last_page", page_name)
''',

    "src/gui/app.py": '''import tkinter as tk

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
'''
}


def main():
    for path, content in files.items():
        file_path = Path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        print(f"Updated: {file_path}")

    print("\\nV4.4 Central Configuration Manager created successfully.")


if __name__ == "__main__":
    main()
