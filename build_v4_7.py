from pathlib import Path

files = {
    "src/config/settings.py": '''APP_NAME = "GH Workspace Manager"
APP_VERSION = "4.7"
WINDOW_TITLE = f"{APP_NAME} V{APP_VERSION}"

DEFAULT_WINDOW_WIDTH = 1100
DEFAULT_WINDOW_HEIGHT = 700

CONFIG_FILE_NAME = "gh_workspace_config.json"
LOG_FILE_NAME = "gh_workspace.log"
DEFAULT_THEME = "light"
''',

    "src/core/plugin_manager.py": '''class PluginManager:
    def __init__(self, app_state):
        self.app_state = app_state
        self.plugins = []

    def register_plugin(self, plugin):
        self.plugins.append(plugin)
        self.app_state.logger.info(f"Plugin registered: {plugin.name}")

    def get_plugins(self):
        return self.plugins
''',

    "src/plugins/__init__.py": "",

    "src/plugins/base_plugin.py": '''class BasePlugin:
    name = "Base Plugin"
    page_key = "base"
    button_text = "Base"

    def create_page(self, parent, app_state):
        raise NotImplementedError("Plugins must implement create_page()")
''',

    "src/plugins/dashboard_plugin.py": '''from plugins.base_plugin import BasePlugin
from gui.pages.dashboard_page import DashboardPage


class DashboardPlugin(BasePlugin):
    name = "Dashboard Plugin"
    page_key = "dashboard"
    button_text = "Dashboard"

    def create_page(self, parent, app_state):
        return DashboardPage(parent, app_state)
''',

    "src/plugins/git_plugin.py": '''from plugins.base_plugin import BasePlugin
from gui.pages.git_page import GitPage


class GitPlugin(BasePlugin):
    name = "Git Manager Plugin"
    page_key = "git"
    button_text = "Git Manager"

    def create_page(self, parent, app_state):
        return GitPage(parent, app_state)
''',

    "src/gui/app.py": '''import tkinter as tk

from config.settings import WINDOW_TITLE, DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT
from core.app_state import AppState
from core.plugin_manager import PluginManager
from gui.theme_manager import ThemeManager
from plugins.dashboard_plugin import DashboardPlugin
from plugins.git_plugin import GitPlugin


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

    def create_sidebar(self):
        self.sidebar_title = tk.Label(
            self.sidebar,
            text="GH Workspace",
            font=("Arial", 14, "bold")
        )
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

        self.theme_button = tk.Button(
            self.sidebar,
            text="Toggle Theme",
            width=20,
            command=self.toggle_theme
        )
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

        self.sidebar_title.configure(
            bg=theme["sidebar_bg"],
            fg=theme["fg"]
        )

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
'''
}


def main():
    for path, content in files.items():
        file_path = Path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        print(f"Updated: {file_path}")

    print("\\nV4.7 Plugin Framework created successfully.")


if __name__ == "__main__":
    main()
