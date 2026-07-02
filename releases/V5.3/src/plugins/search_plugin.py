from plugins.base_plugin import BasePlugin
from gui.pages.search_page import SearchPage


class SearchPlugin(BasePlugin):
    name = "Search Plugin"
    page_key = "search"
    button_text = "Search"

    def create_page(self, parent, app_state):
        return SearchPage(parent, app_state)
