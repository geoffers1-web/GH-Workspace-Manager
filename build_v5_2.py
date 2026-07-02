from pathlib import Path

def write(path, content):
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content.strip() + "\n", encoding="utf-8")
    print(f"Updated: {file_path}")

write("src/config/settings.py", """
APP_NAME = "GH Workspace Manager"
APP_VERSION = "5.2"
BUILDER_VERSION = "1.0"
WINDOW_TITLE = f"{APP_NAME} V{APP_VERSION}"

DEFAULT_WINDOW_WIDTH = 1100
DEFAULT_WINDOW_HEIGHT = 700

CONFIG_FILE_NAME = "gh_workspace_config.json"
LOG_FILE_NAME = "gh_workspace.log"
DEFAULT_THEME = "light"
""")

write("src/services/project_service.py", """
from pathlib import Path
from datetime import datetime


class ProjectService:
    def __init__(self, workspace_path: Path, logger=None):
        self.workspace_path = Path(workspace_path)
        self.logger = logger

    def discover_projects(self):
        projects = []

        if not self.workspace_path.exists():
            return projects

        for path in self.workspace_path.rglob("*"):
            if not path.is_dir():
                continue

            is_git = (path / ".git").exists()
            has_python = any(path.glob("*.py")) or (path / "src").exists()
            has_readme = (path / "README.md").exists()
            has_gitignore = (path / ".gitignore").exists()

            if is_git or has_python or has_readme:
                projects.append({
                    "name": path.name,
                    "path": str(path),
                    "is_git": is_git,
                    "has_python": has_python,
                    "has_readme": has_readme,
                    "has_gitignore": has_gitignore,
                    "last_modified": self.get_last_modified(path),
                    "health": self.get_project_health(is_git, has_readme, has_gitignore),
                })

        projects.sort(key=lambda item: item["name"].lower())

        if self.logger:
            self.logger.info(f"Project discovery completed: {len(projects)} projects found")

        return projects

    def get_last_modified(self, path):
        try:
            timestamp = path.stat().st_mtime
            return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M")
        except Exception:
            return "Unknown"

    def get_project_health(self, is_git, has_readme, has_gitignore):
        if is_git and has_readme and has_gitignore:
            return "Healthy"
        if is_git and has_readme:
            return "Needs .gitignore"
        if is_git and has_gitignore:
            return "Needs README"
        if is_git:
            return "Needs documentation"
        return "Local project"
""")

write("src/gui/pages/project_page.py", """
import tkinter as tk
from tkinter import filedialog
from pathlib import Path

from core.paths import PROJECT_ROOT
from services.project_service import ProjectService


class ProjectPage(tk.Frame):
    def __init__(self, parent, app_state):
        super().__init__(parent)
        self.app_state = app_state
        self.workspace_path = PROJECT_ROOT
        self.projects = []

        self.title = tk.Label(self, text="Project Explorer", font=("Arial", 18, "bold"))
        self.title.pack(pady=15)

        self.path_label = tk.Label(self, text=f"Workspace: {self.workspace_path}", font=("Arial", 10))
        self.path_label.pack(pady=5)

        self.button_frame = tk.Frame(self)
        self.button_frame.pack(pady=5)

        self.choose_button = tk.Button(
            self.button_frame,
            text="Choose Workspace",
            command=self.choose_workspace
        )
        self.choose_button.pack(side="left", padx=5)

        self.scan_button = tk.Button(
            self.button_frame,
            text="Discover Projects",
            command=self.discover_projects
        )
        self.scan_button.pack(side="left", padx=5)

        self.main_frame = tk.Frame(self)
        self.main_frame.pack(expand=True, fill="both", padx=10, pady=10)

        self.listbox = tk.Listbox(self.main_frame, width=40)
        self.listbox.pack(side="left", fill="both", expand=False)
        self.listbox.bind("<<ListboxSelect>>", self.show_selected_project)

        self.details = tk.Text(self.main_frame, height=24, width=70)
        self.details.pack(side="right", fill="both", expand=True, padx=10)

    def choose_workspace(self):
        selected = filedialog.askdirectory(title="Choose GH Workspace Folder")
        if selected:
            self.workspace_path = Path(selected)
            self.path_label.configure(text=f"Workspace: {self.workspace_path}")

    def discover_projects(self):
        service = ProjectService(self.workspace_path, self.app_state.logger)
        self.projects = service.discover_projects()

        self.listbox.delete(0, tk.END)
        self.details.delete("1.0", tk.END)

        for project in self.projects:
            self.listbox.insert(tk.END, project["name"])

        self.details.insert(tk.END, f"Projects found: {len(self.projects)}")

    def show_selected_project(self, event=None):
        selection = self.listbox.curselection()

        if not selection:
            return

        project = self.projects[selection[0]]
        report = self.format_project_details(project)

        self.details.delete("1.0", tk.END)
        self.details.insert(tk.END, report)

    def yes_no(self, value):
        return "Yes" if value else "No"

    def format_project_details(self, project):
        return f'''Project Details

Name:
{project["name"]}

Path:
{project["path"]}

Git Repository:
{self.yes_no(project["is_git"])}

Python Project:
{self.yes_no(project["has_python"])}

README.md:
{self.yes_no(project["has_readme"])}

.gitignore:
{self.yes_no(project["has_gitignore"])}

Last Modified:
{project["last_modified"]}

Health:
{project["health"]}
'''

    def apply_theme(self, theme):
        self.configure(bg=theme["content_bg"])
        self.title.configure(bg=theme["content_bg"], fg=theme["fg"])
        self.path_label.configure(bg=theme["content_bg"], fg=theme["fg"])
        self.button_frame.configure(bg=theme["content_bg"])
        self.main_frame.configure(bg=theme["content_bg"])

        for button in [self.choose_button, self.scan_button]:
            button.configure(
                bg=theme["button_bg"],
                fg=theme["button_fg"],
                activebackground=theme["content_bg"],
                activeforeground=theme["fg"]
            )

        self.listbox.configure(
            bg=theme["text_bg"],
            fg=theme["text_fg"]
        )

        self.details.configure(
            bg=theme["text_bg"],
            fg=theme["text_fg"],
            insertbackground=theme["text_fg"]
        )
""")

write("src/plugins/project_plugin.py", """
from plugins.base_plugin import BasePlugin
from gui.pages.project_page import ProjectPage


class ProjectPlugin(BasePlugin):
    name = "Project Explorer Plugin"
    page_key = "projects"
    button_text = "Project Explorer"

    def create_page(self, parent, app_state):
        return ProjectPage(parent, app_state)
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
from plugins.health_plugin import HealthPlugin
from plugins.project_plugin import ProjectPlugin


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
        self.plugin_manager.register_plugin(HealthPlugin())
        self.plugin_manager.register_plugin(ProjectPlugin())

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

write("docs/releases/V5.2_RELEASE_NOTES.md", """
# V5.2 Release Notes

V5.2 adds the Project Explorer.

Added:
- ProjectService
- Project Explorer page
- Project Explorer plugin
- Project discovery
- Project detail panel
- Project health status
""")

write("docs/user/V5.2_USER_GUIDE.md", """
# V5.2 User Guide

## Project Explorer

Open GH Workspace Manager:

python src/main.py

Click Project Explorer.

Use Discover Projects to scan the current workspace.

Use Choose Workspace to select a different folder.

Select a project from the list to view:
- Path
- Git status
- Python project detection
- README status
- .gitignore status
- Last modified time
- Health result
""")

write("docs/developer/V5.2_DEVELOPER_GUIDE.md", """
# V5.2 Developer Guide

V5.2 adds ProjectService.

Files added:
- src/services/project_service.py
- src/gui/pages/project_page.py
- src/plugins/project_plugin.py

The Project Explorer follows the established service/page/plugin pattern.
""")

write("docs/roadmap/V5.2_ROADMAP.md", """
# Roadmap

## Completed in V5.2

- Project Explorer
- Project discovery
- Project health summaries

## Next

- V5.3 Search & Indexing
- V5.4 Documentation Manager
- V5.5 Backup & Restore
""")

write("docs/V5.2_TEST_CHECKLIST.md", """
# V5.2 Test Checklist

Run:

python build_v5_2.py
python src/main.py

## Application

- App opens as V5.2
- Dashboard works
- Git Manager works
- Workspace Scanner works
- Health Center works
- Project Explorer button appears
- Project Explorer opens
- Discover Projects works
- Project list appears
- Selecting a project shows details
- Theme toggle works
- Theme persists after reopening
""")

write("README.md", """
# GH Workspace Manager

Current Version: V5.2 - Project Explorer

GH Workspace Manager is a modular desktop application for managing a GitHub-based local workspace.

## Features

- Modular architecture
- Configuration manager
- Logging framework
- Theme manager
- Plugin framework
- Dashboard
- Git Manager
- Workspace Scanner
- Health Center
- Project Explorer
- Release package structure
- GH Workspace Builder
- Versioned documentation

## Run Application

python src/main.py

## Run Builder

python Builder/builder.py
""")

write("CHANGELOG.md", """
# Changelog

## V5.2 - Project Explorer

Added:
- ProjectService
- Project Explorer page
- Project Explorer plugin
- Project discovery
- Project details panel
- Project health status

## V5.1 - System Information & Health Center

Added:
- SystemInfoService
- Health Center page
- Health Center plugin
- Health check report
- Versioned documentation

## V5.0 - GH Workspace Builder

Added:
- Builder/builder.py
- Project validation
- Import verification
- Release snapshot creation
""")

print()
print("V5.2 Project Explorer installed successfully.")
print("Next run: python src/main.py")
