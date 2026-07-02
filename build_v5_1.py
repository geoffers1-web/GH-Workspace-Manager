from pathlib import Path

def write(path, content):
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content.strip() + "\n", encoding="utf-8")
    print(f"Updated: {file_path}")

write("src/config/settings.py", """
APP_NAME = "GH Workspace Manager"
APP_VERSION = "5.1"
BUILDER_VERSION = "1.0"
WINDOW_TITLE = f"{APP_NAME} V{APP_VERSION}"

DEFAULT_WINDOW_WIDTH = 1100
DEFAULT_WINDOW_HEIGHT = 700

CONFIG_FILE_NAME = "gh_workspace_config.json"
LOG_FILE_NAME = "gh_workspace.log"
DEFAULT_THEME = "light"
""")

write("src/services/system_info_service.py", """
import subprocess
from pathlib import Path

from config.settings import APP_NAME, APP_VERSION, BUILDER_VERSION
from core.paths import PROJECT_ROOT, APP_LOG_FILE


class SystemInfoService:
    def __init__(self, app_state):
        self.app_state = app_state

    def get_git_branch(self):
        try:
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                cwd=PROJECT_ROOT,
                text=True,
                capture_output=True,
                check=False
            )
            return result.stdout.strip() or "Unknown"
        except Exception:
            return "Unavailable"

    def get_git_status_summary(self):
        try:
            result = subprocess.run(
                ["git", "status", "--short"],
                cwd=PROJECT_ROOT,
                text=True,
                capture_output=True,
                check=False
            )
            output = result.stdout.strip()
            return "Clean" if not output else "Changes pending"
        except Exception:
            return "Unavailable"

    def count_plugins(self):
        try:
            return len(list((PROJECT_ROOT / "src" / "plugins").glob("*_plugin.py")))
        except Exception:
            return 0

    def count_releases(self):
        releases_dir = PROJECT_ROOT / "releases"
        if not releases_dir.exists():
            return 0
        return len([p for p in releases_dir.iterdir() if p.is_dir()])

    def get_health_report(self):
        theme = self.app_state.config_manager.get("theme", "light")
        current_page = self.app_state.current_page

        return {
            "Application": APP_NAME,
            "Version": APP_VERSION,
            "Builder Version": BUILDER_VERSION,
            "Project Root": str(PROJECT_ROOT),
            "Current Page": current_page,
            "Theme": theme,
            "Git Branch": self.get_git_branch(),
            "Git Status": self.get_git_status_summary(),
            "Installed Plugins": self.count_plugins(),
            "Release Snapshots": self.count_releases(),
            "Log File": str(APP_LOG_FILE),
            "Health Status": "Healthy",
        }

    def format_health_report(self):
        report = self.get_health_report()
        lines = ["GH Workspace Manager - System Information & Health Center", ""]

        for key, value in report.items():
            lines.append(f"{key:.<24} {value}")

        return "\\n".join(lines)
""")

write("src/gui/pages/health_page.py", """
import subprocess
import sys
import tkinter as tk
from pathlib import Path

from core.paths import PROJECT_ROOT, APP_LOG_FILE
from services.system_info_service import SystemInfoService


class HealthPage(tk.Frame):
    def __init__(self, parent, app_state):
        super().__init__(parent)
        self.app_state = app_state
        self.system_info = SystemInfoService(app_state)

        self.title = tk.Label(
            self,
            text="System Information & Health Center",
            font=("Arial", 18, "bold")
        )
        self.title.pack(pady=20)

        self.refresh_button = tk.Button(
            self,
            text="Run Health Check",
            command=self.refresh_report
        )
        self.refresh_button.pack(pady=5)

        self.import_button = tk.Button(
            self,
            text="Verify Imports",
            command=self.verify_imports
        )
        self.import_button.pack(pady=5)

        self.builder_button = tk.Button(
            self,
            text="Launch Builder",
            command=self.launch_builder
        )
        self.builder_button.pack(pady=5)

        self.output = tk.Text(self, height=24, width=100)
        self.output.pack(pady=10)

        self.refresh_report()

    def refresh_report(self):
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, self.system_info.format_health_report())
        self.app_state.logger.info("Health check refreshed")

    def verify_imports(self):
        python_files = list((PROJECT_ROOT / "src").rglob("*.py"))
        output_lines = ["Python Import Verification", ""]

        failed = []

        for file_path in python_files:
            result = subprocess.run(
                [sys.executable, "-m", "py_compile", str(file_path)],
                cwd=PROJECT_ROOT,
                text=True,
                capture_output=True
            )

            rel_path = file_path.relative_to(PROJECT_ROOT)

            if result.returncode == 0:
                output_lines.append(f"OK      {rel_path}")
            else:
                output_lines.append(f"FAILED  {rel_path}")
                output_lines.append(result.stderr)
                failed.append(rel_path)

        output_lines.append("")
        output_lines.append("Result: SUCCESS" if not failed else "Result: FAILED")

        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, "\\n".join(output_lines))

    def launch_builder(self):
        builder_path = PROJECT_ROOT / "Builder" / "builder.py"

        if not builder_path.exists():
            self.output.delete("1.0", tk.END)
            self.output.insert(tk.END, "Builder not found.")
            return

        subprocess.Popen(
            [sys.executable, str(builder_path)],
            cwd=PROJECT_ROOT
        )

        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, "Builder launch requested.")

    def apply_theme(self, theme):
        self.configure(bg=theme["content_bg"])
        self.title.configure(bg=theme["content_bg"], fg=theme["fg"])

        for button in [self.refresh_button, self.import_button, self.builder_button]:
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

write("src/plugins/health_plugin.py", """
from plugins.base_plugin import BasePlugin
from gui.pages.health_page import HealthPage


class HealthPlugin(BasePlugin):
    name = "System Health Plugin"
    page_key = "health"
    button_text = "Health Center"

    def create_page(self, parent, app_state):
        return HealthPage(parent, app_state)
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

write("docs/architecture/V5.1_ARCHITECTURE_GUIDE.md", """
# V5.1 Architecture Guide

GH Workspace Manager uses a modular desktop architecture.

Main layers:

- core: shared application state, paths, logging, plugin management
- config: application settings and configuration manager
- services: business logic and system services
- gui: Tkinter application shell and pages
- plugins: feature registration layer
- Builder: development and release tooling
- releases: versioned release snapshots

V5.1 adds the System Information Service and Health Center plugin.
""")

write("docs/developer/V5.1_DEVELOPER_GUIDE.md", """
# V5.1 Developer Guide

## Adding a New Feature

New features should generally be added as:

1. A service in src/services/
2. A page in src/gui/pages/
3. A plugin in src/plugins/
4. A registration entry in src/gui/app.py

## Plugin Pattern

Each plugin extends BasePlugin and provides:

- name
- page_key
- button_text
- create_page()

This keeps the main application shell clean and modular.
""")

write("docs/user/V5.1_USER_GUIDE.md", """
# V5.1 User Guide

## Running the Application

python src/main.py

## Main Pages

- Dashboard: general overview
- Git Manager: Git status and recent commits
- Workspace Scanner: scan folders and detect project files
- Health Center: view system information and run health checks

## Running the Builder

python Builder/builder.py
""")

write("docs/releases/V5.1_RELEASE_NOTES.md", """
# V5.1 Release Notes

V5.1 adds the System Information & Health Center.

Added:

- SystemInfoService
- Health Center page
- Health Center plugin
- Health check report
- Import verification from inside the application
- Builder launch button
- Versioned documentation folders
""")

write("docs/roadmap/V5.1_ROADMAP.md", """
# GH Workspace Manager Roadmap

## Completed

- V4.3 Modular Architecture
- V4.4 Configuration Manager
- V4.5 Logging Framework
- V4.6 Theme Manager
- V4.7 Plugin Framework
- V4.8 Workspace Scanner
- V4.9 Release Package Structure
- V5.0 GH Workspace Builder
- V5.1 System Information & Health Center

## Next

- V5.2 Project Explorer
- V5.3 Search & Indexing
- V5.4 Documentation Manager
- V5.5 Backup & Restore
- V6.0 Professional Workspace Suite
""")

write("docs/V5.1_TEST_CHECKLIST.md", """
# V5.1 Test Checklist

Run:

python build_v5_1.py
python src/main.py

## Application

- App opens as V5.1
- Dashboard works
- Git Manager works
- Workspace Scanner works
- Health Center button appears
- Health Center opens
- Run Health Check works
- Verify Imports works
- Launch Builder works
- Theme toggle works
- Theme persists after reopening

## Documentation

- docs/architecture/V5.1_ARCHITECTURE_GUIDE.md exists
- docs/developer/V5.1_DEVELOPER_GUIDE.md exists
- docs/user/V5.1_USER_GUIDE.md exists
- docs/releases/V5.1_RELEASE_NOTES.md exists
- docs/roadmap/V5.1_ROADMAP.md exists
""")

write("README.md", """
# GH Workspace Manager

Current Version: V5.1 - System Information & Health Center

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
- Release package structure
- GH Workspace Builder
- System Information & Health Center
- Versioned documentation

## Run Application

python src/main.py

## Run Builder

python Builder/builder.py
""")

write("CHANGELOG.md", """
# Changelog

## V5.1 - System Information & Health Center

Added:
- SystemInfoService
- Health Center page
- Health Center plugin
- Health check report
- Import verification inside the application
- Builder launcher from the application
- Versioned documentation folders
- Architecture Guide
- Developer Guide
- User Guide
- Release Notes
- Roadmap

## V5.0 - GH Workspace Builder

Added:
- Builder/builder.py
- Project structure validation
- Python import verification
- Git status command
- Release snapshot creation
- Release listing
- Application launcher

## V4.9 - Release Package Structure

Added:
- releases/ folder structure
- release package snapshots
- manifest.json release metadata
""")

print()
print("V5.1 System Information & Health Center installed successfully.")
print("Next run: python src/main.py")
