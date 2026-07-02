class PluginManager:
    def __init__(self, app_state):
        self.app_state = app_state
        self.plugins = []

    def register_plugin(self, plugin):
        self.plugins.append(plugin)
        self.app_state.logger.info(f"Plugin registered: {plugin.name}")

    def get_plugins(self):
        return self.plugins
