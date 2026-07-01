from config.config_manager import ConfigManager
from core.paths import APP_CONFIG_FILE


class AppState:
    def __init__(self):
        self.config_manager = ConfigManager(APP_CONFIG_FILE)
        self.current_page = self.config_manager.get("last_page", "dashboard")
        self.status_message = "Ready"

    def set_current_page(self, page_name):
        self.current_page = page_name
        self.config_manager.set("last_page", page_name)
