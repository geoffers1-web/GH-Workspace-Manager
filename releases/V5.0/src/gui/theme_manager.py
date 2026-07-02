class ThemeManager:
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
