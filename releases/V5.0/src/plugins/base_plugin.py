class BasePlugin:
    name = "Base Plugin"
    page_key = "base"
    button_text = "Base"

    def create_page(self, parent, app_state):
        raise NotImplementedError("Plugins must implement create_page()")
