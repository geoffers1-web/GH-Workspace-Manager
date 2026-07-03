import tkinter as tk

from gui.preferences_dialog import PreferencesDialog
from config.settings import DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT
from core.app_metadata import APP_NAME, APP_RELEASE, APP_AUTHOR, APP_DESCRIPTION, get_window_title
from core.app_state import AppState
from core.plugin_manager import PluginManager
from gui.theme_manager import ThemeManager
from plugins.dashboard_plugin import DashboardPlugin
from plugins.git_plugin import GitPlugin
from plugins.workspace_plugin import WorkspacePlugin
from plugins.health_plugin import HealthPlugin
from plugins.project_plugin import ProjectPlugin
from plugins.search_plugin import SearchPlugin


class GHWorkspaceApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.app_state = AppState()
        self.theme_manager = ThemeManager(self.app_state)
        self.plugin_manager = PluginManager(self.app_state)

        width = self.app_state.config_manager.get("window_width", DEFAULT_WINDOW_WIDTH)
        height = self.app_state.config_manager.get("window_height", DEFAULT_WINDOW_HEIGHT)

        self.title(get_window_title())
        self.geometry(f"{width}x{height}")

        self.sidebar = tk.Frame(self, width=200)
        self.sidebar.pack(side="left", fill="y")

        self.main_area = tk.Frame(self)
        self.main_area.pack(side="right", expand=True, fill="both")

        self.content = tk.Frame(self.main_area)
        self.content.pack(side="top", expand=True, fill="both")

        self.status_bar = tk.Label(
            self.main_area,
            text=self.get_status_text(),
            anchor="w",
            relief="sunken",
            padx=8
        )
        self.status_bar.pack(side="bottom", fill="x")

        self.pages = {}
        self.buttons = []

        self.register_plugins()
        self.create_menu_bar()
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
        self.plugin_manager.register_plugin(SearchPlugin())

    def create_menu_bar(self):
        menu_bar = tk.Menu(self)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        view_menu = tk.Menu(menu_bar, tearoff=0)
        for plugin in self.plugin_manager.get_plugins():
            view_menu.add_command(
                label=plugin.button_text,
                command=lambda page_key=plugin.page_key: self.show_page(page_key)
            )
        menu_bar.add_cascade(label="View", menu=view_menu)

        tools_menu = tk.Menu(menu_bar, tearoff=0)
        tools_menu.add_command(label="Toggle Theme", command=self.toggle_theme)
        tools_menu.add_separator()
        tools_menu.add_command(label="Preferences", command=self.open_preferences)
        menu_bar.add_cascade(label="Tools", menu=tools_menu)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        self.config(menu=menu_bar)

    def create_sidebar(self):
        self.sidebar_title = tk.Label(
            self.sidebar,
            text=f"{APP_NAME} {APP_RELEASE}",
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

        self.about_button = tk.Button(
            self.sidebar,
            text="About",
            width=20,
            command=self.show_about
        )
        self.about_button.pack(pady=5)
        self.buttons.append(self.about_button)

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
        self.update_status_bar()

    def toggle_theme(self):
        current_theme = self.theme_manager.get_theme_name()
        new_theme = "dark" if current_theme == "light" else "light"
        self.theme_manager.set_theme_name(new_theme)
        self.apply_theme()
        self.update_status_bar()

    def get_status_text(self):
        theme_name = self.theme_manager.get_theme_name().title()
        current_page = self.app_state.current_page.title()
        return f"Ready | Page: {current_page} | Theme: {theme_name} | Version: {APP_RELEASE}"

    def open_preferences(self):
        PreferencesDialog(self, on_save=self.on_preferences_saved)

    def on_preferences_saved(self, settings):
        self.update_status_bar()
        self.status_bar.configure(text="Preferences saved.")

    def update_status_bar(self):
        self.status_bar.configure(text=self.get_status_text())

    def show_about(self):
        about_window = tk.Toplevel(self)
        about_window.title(f"About {APP_NAME}")
        about_window.geometry("420x220")
        about_window.resizable(False, False)

        theme = self.theme_manager.get_theme()
        about_window.configure(bg=theme["bg"])

        title = tk.Label(
            about_window,
            text=f"{APP_NAME} {APP_RELEASE}",
            font=("Arial", 16, "bold"),
            bg=theme["bg"],
            fg=theme["fg"]
        )
        title.pack(pady=(20, 10))

        description = tk.Label(
            about_window,
            text=APP_DESCRIPTION,
            wraplength=360,
            bg=theme["bg"],
            fg=theme["fg"]
        )
        description.pack(pady=5)

        author = tk.Label(
            about_window,
            text=f"Author: {APP_AUTHOR}",
            bg=theme["bg"],
            fg=theme["fg"]
        )
        author.pack(pady=10)

    def apply_theme(self):
        theme = self.theme_manager.get_theme()

        self.configure(bg=theme["bg"])
        self.sidebar.configure(bg=theme["sidebar_bg"])
        self.main_area.configure(bg=theme["content_bg"])
        self.content.configure(bg=theme["content_bg"])

        self.status_bar.configure(
            bg=theme["sidebar_bg"],
            fg=theme["fg"]
        )

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

        self.update_status_bar()
