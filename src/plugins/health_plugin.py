from plugins.base_plugin import BasePlugin
from gui.pages.health_page import HealthPage


class HealthPlugin(BasePlugin):
    name = "System Health Plugin"
    page_key = "health"
    button_text = "Health Center"

    def create_page(self, parent, app_state):
        return HealthPage(parent, app_state)
