from pathlib import Path

def write(path, content):
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content.strip() + "\n", encoding="utf-8")
    print(f"Updated: {file_path}")

write("src/config/settings.py", """
APP_NAME = "GH Workspace Manager"
APP_VERSION = "4.8"
WINDOW_TITLE = f"{APP_NAME} V{APP_VERSION}"

DEFAULT_WINDOW_WIDTH = 1100
DEFAULT_WINDOW_HEIGHT = 700

CONFIG_FILE_NAME = "gh_workspace_config.json"
LOG_FILE_NAME = "gh_workspace.log"
DEFAULT_THEME = "light"
""")

write("src/services/workspace_service.py", """
from pathlib import Path


class WorkspaceService:
    def __init__(self, workspace_path: Path, logger=None):
        self.workspace_path = Path(workspace_path)
        self.logger = logger

    def scan_workspace(self):
        results = {
            "workspace_path": str(self.workspace_path),
            "total_folders": 0,
            "total_files": 0,
            "git_repositories": 0,
            "python_files": 0,
            "bash_scripts": 0,
            "markdown_docs": 0,
            "pdf_files": 0,
            "image_files": 0,
            "projects_missing_readme": [],
            "projects_missing_gitignore": [],
        }

        if not self.workspace_path.exists():
            return results

        for path in self.workspace_path.rglob("*"):
            if path.is_dir():
                results["total_folders"] += 1

                if (path / ".git").exists():
                    results["git_repositories"] += 1

                    if not (path / "README.md").exists():
                        results["projects_missing_readme"].append(str(path))

                    if not (path / ".gitignore").exists():
                        results["projects_missing_gitignore"].append(str(path))

            elif path.is_file():
                results["total_files"] += 1
                suffix = path.suffix.lower()

                if suffix == ".py":
                    results["python_files"] += 1
                elif suffix == ".sh":
                    results["bash_scripts"] += 1
                elif suffix in [".md", ".txt", ".rst"]:
                    results["markdown_docs"] += 1
                elif suffix == ".pdf":
                    results["pdf_files"] += 1
                elif suffix in [".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"]:
                    results["image_files"] += 1

        if self.logger:
            self.logger.info("Workspace scan completed")

        return results
""")

write("src/gui/pages/workspace_page.py", """
import tkinter as tk
from tkinter import filedialog

from services.workspace_service import WorkspaceService
from core.paths import PROJECT_ROOT


class WorkspacePage(tk.Frame):
    def __init__(self, parent, app_state):
        super().__init__(parent)
        self.app_state = app_state
        self.workspace_path = PROJECT_ROOT

        self.title = tk.Label(self, text="Workspace Scanner & Project Explorer", font=("Arial", 18, "bold"))
        self.title.pack(pady=20)

        self.path_label = tk.Label(self, text=f"Workspace: {self.workspace_path}", font=("Arial", 10))
        self.path_label.pack(pady=5)

        self.choose_button = tk.Button(self, text="Choose Workspace Folder", command=self.choose_workspace)
        self.choose_button.pack(pady=5)

        self.scan_button = tk.Button(self, text="Scan Workspace", command=self.scan_workspace)
        self.scan_button.pack(pady=5)

        self.output = tk.Text(self, height=24, width=100)
        self.output.pack(pady=10)

    def choose_workspace(self):
        selected = filedialog.askdirectory(title="Choose GH Workspace Folder")
        if selected:
            self.workspace_path = selected
            self.path_label.configure(text=f"Workspace: {self.workspace_path}")

    def scan_workspace(self):
        service = WorkspaceService(self.workspace_path, self.app_state.logger)
        results = service.scan_workspace()
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, self.format_report(results))

    def format_report(self, results):
        missing_readme = "\\n".join(results["projects_missing_readme"][:10]) or "None"
        missing_gitignore = "\\n".join(results["projects_missing_gitignore"][:10]) or "None"

        return f'''GH Workspace Scan Report

Workspace:
{results["workspace_path"]}

Summary:
Folders ................ {results["total_folders"]}
Files .................. {results["total_files"]}
Git Repositories ....... {results["git_repositories"]}
Python Files ........... {results["python_files"]}
Bash Scripts ........... {results["bash_scripts"]}
Documents .............. {results["markdown_docs"]}
PDF Files .............. {results["pdf_files"]}
Image Files ............ {results["image_files"]}

Projects Missing README.md:
{missing_readme}

Projects Missing .gitignore:
{missing_gitignore}
'''

    def apply_theme(self, theme):
        self.configure(bg=theme["content_bg"])

        for widget in [self.title, self.path_label]:
            widget.configure(bg=theme["content_bg"], fg=theme["fg"])

        for button in [self.choose_button, self.scan_button]:
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
""")

write("src/plugins/workspace_plugin.py", """
from plugins.base_plugin import BasePlugin
from gui.pages.workspace_page import WorkspacePage


class WorkspacePlugin(BasePlugin):
    name = "Workspace Scanner Plugin"
    page_key = "workspace"
    button_text = "Workspace Scanner"

    def create_page(self, parent, app_state):
        return WorkspacePage(parent, app_state)
""")

write("src/gui/app.py", """
import tkinter as tk

from config.settings import WINDOW_TITLE, DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT
from core.app_state import AppState
from core.plugin_manager import PluginManager
from gui.theme_manager import ThemeManager
from plugins.dashboard_plugin import DashboardPlugin
from plugins.git_plugin import GitPlugin
from plugins.workspace_plugin import WorkspacePlugin


class GHWorkspaceApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.app_state = AppState()
        self.theme_manager = ThemeManager(self.app_state)
        self.plugin_manager = PluginManager(self.app_state)

        width = self.app_state.config_manager.get("window_width", DEFAULT_WINDOW_WIDTH)
        height = self.app_state.config_manager.get("window_height", DEFAULT_WINDOW_HEIGHT)

        self.title(WINDOW_TITLE)
        self.geometry(f"{width}x{height}")

        self.sidebar = tk.Frame(self, width=200)
        self.sidebar.pack(side="left", fill="y")

        self.content = tk.Frame(self)
        self.content.pack(side="right", expand=True, fill="both")

        self.pages = {}
        self.buttons = []

        self.register_plugins()
        self.create_sidebar()
        self.create_pages()
        self.apply_theme()
        self.show_page(self.app_state.current_page)

    def register_plugins(self):
        self.plugin_manager.register_plugin(DashboardPlugin())
        self.plugin_manager.register_plugin(GitPlugin())
        self.plugin_manager.register_plugin(WorkspacePlugin())

    def create_sidebar(self):
        self.sidebar_title = tk.Label(self.sidebar, text="GH Workspace", font=("Arial", 14, "bold"))
        self.sidebar_title.pack(pady=20)

        for plugin in self.plugin_manager.get_plugins():
            button = tk.Button(
                self.sidebar,
                text=plugin.button_text,
                width=20,
                command=lambda page_key=plugin.page_key: self.show_page(page_key)
            )
            button.pack(pady=5)
            self.buttons.append(button)

        self.theme_button = tk.Button(self.sidebar, text="Toggle Theme", width=20, command=self.toggle_theme)
        self.theme_button.pack(pady=25)
        self.buttons.append(self.theme_button)

    def create_pages(self):
        for plugin in self.plugin_manager.get_plugins():
            self.pages[plugin.page_key] = plugin.create_page(self.content, self.app_state)

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

        self.sidebar_title.configure(bg=theme["sidebar_bg"], fg=theme["fg"])

        for button in self.buttons:
            button.configure(
                bg=theme["button_bg"],
                fg=theme["button_fg"],
                activebackground=theme["content_bg"],
                activeforeground=theme["fg"]
            )

        for page in self.pages.values():
            if hasattr(page, "apply_theme"):
                page.apply_theme(theme)
""")

write("README.md", """
# GH Workspace Manager

Current Version: V4.8 - Workspace Scanner & Project Explorer

Features:
- Modular architecture
- Configuration manager
- Logging framework
- Theme manager
- Plugin framework
- Dashboard
- Git Manager
- Workspace Scanner

Run:
python src/main.py
""")

write("CHANGELOG.md", """
# Changelog

## V4.8 - Workspace Scanner & Project Explorer

Added:
- Workspace Scanner plugin
- Workspace Scanner page
- Workspace scanning service
- Git repository detection
- File type counting
- Missing README.md detection
- Missing .gitignore detection
""")

write("docs/V4.8_TEST_CHECKLIST.md", """
# V4.8 Test Checklist

- App opens as V4.8
- Dashboard button works
- Git Manager button works
- Workspace Scanner button appears
- Workspace Scanner button works
- Toggle Theme works
- Theme is remembered after reopening
- Choose Workspace Folder opens folder picker
- Scan Workspace creates a report
- Git status still works
- Recent commits still works
""")

print()
print("V4.8 fix installed successfully.")
print("Next run: python src/main.py")
