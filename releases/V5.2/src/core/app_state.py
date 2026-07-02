from config.config_manager import ConfigManager
from core.paths import APP_CONFIG_FILE
from core.logger import app_logger


class AppState:
    def __init__(self):
        self.logger = app_logger
        self.logger.info("Starting GH Workspace Manager")

        self.config_manager = ConfigManager(APP_CONFIG_FILE)
        self.current_page = self.config_manager.get("last_page", "dashboard")
        self.status_message = "Ready"

    def set_current_page(self, page_name):
        self.current_page = page_name
        self.config_manager.set("last_page", page_name)
        self.logger.info(f"Page changed to: {page_name}")
