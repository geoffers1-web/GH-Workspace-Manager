from plugins.base_plugin import BasePlugin
from gui.pages.git_page import GitPage


class GitPlugin(BasePlugin):
    name = "Git Manager Plugin"
    page_key = "git"
    button_text = "Git Manager"

    def create_page(self, parent, app_state):
        return GitPage(parent, app_state)
