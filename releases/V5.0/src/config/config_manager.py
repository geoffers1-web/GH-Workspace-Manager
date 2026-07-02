import json
from pathlib import Path


class ConfigManager:
    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.default_config = {
            "app_name": "GH Workspace Manager",
            "version": "4.4",
            "theme": "light",
            "last_page": "dashboard",
            "window_width": 1100,
            "window_height": 700
        }
        self.config = self.load_config()

    def load_config(self):
        if not self.config_path.exists():
            self.save_config(self.default_config)
            return self.default_config.copy()

        try:
            with self.config_path.open("r", encoding="utf-8") as file:
                loaded = json.load(file)

            config = self.default_config.copy()
            config.update(loaded)
            return config

        except Exception:
            self.save_config(self.default_config)
            return self.default_config.copy()

    def save_config(self, config=None):
        if config is None:
            config = self.config

        self.config_path.parent.mkdir(parents=True, exist_ok=True)

        with self.config_path.open("w", encoding="utf-8") as file:
            json.dump(config, file, indent=4)

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        self.save_config()
