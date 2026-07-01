from pathlib import Path

files = {
    "src/config/settings.py": '''APP_NAME = "GH Workspace Manager"
APP_VERSION = "4.3"
WINDOW_TITLE = f"{APP_NAME} V{APP_VERSION}"

DEFAULT_WINDOW_WIDTH = 1100
DEFAULT_WINDOW_HEIGHT = 700
''',

    "src/core/paths.py": '''from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"
DOCS_DIR = PROJECT_ROOT / "docs"
CONFIG_DIR = SRC_DIR / "config"
''',

    "src/core/app_state.py": '''class AppState:
    def __init__(self):
        self.current_page = "dashboard"
        self.status_message = "Ready"
''',

    "src/services/git_service.py": '''import subprocess
from pathlib import Path


class GitService:
    def __init__(self, repo_path: Path):
        self.repo_path = repo_path

    def run_git_command(self, args):
        try:
            result = subprocess.run(
                ["git"] + args,
                cwd=self.repo_path,
                text=True,
                capture_output=True,
                check=False
            )
            return result.stdout.strip() or result.stderr.strip()
        except Exception as error:
            return f"Git error: {error}"

    def status(self):
        return self.run_git_command(["status"])

    def log(self):
        return self.run_git_command(["log", "--oneline", "-10"])
''',

    "src/gui/pages/dashboard_page.py": '''import tkinter as tk


class DashboardPage(tk.Frame):
    def __init__(self, parent, app_state):
        super().__init__(parent)
        self.app_state = app_state

        title = tk.Label(
            self,
            text="Dashboard & Workspace Health",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=20)

        message = tk.Label(
            self,
            text="GH Workspace Manager professional modular architecture is running.",
            font=("Arial", 12)
        )
        message.pack(pady=10)
''',

    "src/gui/pages/git_page.py": '''import tkinter as tk
from services.git_service import GitService
from core.paths import PROJECT_ROOT


class GitPage(tk.Frame):
    def __init__(self, parent, app_state):
        super().__init__(parent)
        self.app_state = app_state
        self.git_service = GitService(PROJECT_ROOT)

        title = tk.Label(self, text="Git Manager", font=("Arial", 18, "bold"))
        title.pack(pady=20)

        status_button = tk.Button(self, text="Show Git Status", command=self.show_status)
        status_button.pack(pady=5)

        log_button = tk.Button(self, text="Show Recent Commits", command=self.show_log)
        log_button.pack(pady=5)

        self.output = tk.Text(self, height=20, width=100)
        self.output.pack(pady=10)

    def show_status(self):
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, self.git_service.status())

    def show_log(self):
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, self.git_service.log())
''',

    "src/gui/app.py": '''import tkinter as tk

from config.settings import WINDOW_TITLE, DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT
from core.app_state import AppState
from gui.pages.dashboard_page import DashboardPage
from gui.pages.git_page import GitPage


class GHWorkspaceApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title(WINDOW_TITLE)
        self.geometry(f"{DEFAULT_WINDOW_WIDTH}x{DEFAULT_WINDOW_HEIGHT}")

        self.app_state = AppState()

        self.sidebar = tk.Frame(self, width=200)
        self.sidebar.pack(side="left", fill="y")

        self.content = tk.Frame(self)
        self.content.pack(side="right", expand=True, fill="both")

        self.pages = {}

        self.create_sidebar()
        self.create_pages()
        self.show_page("dashboard")

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
        self.app_state.current_page = name
        self.pages[name].tkraise()
''',

    "src/main.py": '''from gui.app import GHWorkspaceApp


def main():
    app = GHWorkspaceApp()
    app.mainloop()


if __name__ == "__main__":
    main()
'''
}


def main():
    for path, content in files.items():
        file_path = Path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        print(f"Created: {file_path}")

    print("\\nV4.3 Professional Modular Architecture files created successfully.")


if __name__ == "__main__":
    main()
