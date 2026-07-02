from plugins.base_plugin import BasePlugin
from gui.pages.dashboard_page import DashboardPage


class DashboardPlugin(BasePlugin):
    name = "Dashboard Plugin"
    page_key = "dashboard"
    button_text = "Dashboard"

    def create_page(self, parent, app_state):
        return DashboardPage(parent, app_state)
