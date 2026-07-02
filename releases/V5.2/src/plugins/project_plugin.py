from plugins.base_plugin import BasePlugin
from gui.pages.project_page import ProjectPage


class ProjectPlugin(BasePlugin):
    name = "Project Explorer Plugin"
    page_key = "projects"
    button_text = "Project Explorer"

    def create_page(self, parent, app_state):
        return ProjectPage(parent, app_state)
