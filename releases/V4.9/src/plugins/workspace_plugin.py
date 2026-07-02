from plugins.base_plugin import BasePlugin
from gui.pages.workspace_page import WorkspacePage


class WorkspacePlugin(BasePlugin):
    name = "Workspace Scanner Plugin"
    page_key = "workspace"
    button_text = "Workspace Scanner"

    def create_page(self, parent, app_state):
        return WorkspacePage(parent, app_state)
