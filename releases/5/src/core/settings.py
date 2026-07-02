import json
from pathlib import Path

DEFAULT_SETTINGS = {
    "workspace_path": str(Path.home() / "GH Workspace")
}

class SettingsManager:
    def __init__(self, config_path=None):
        if config_path is None:
            self.config_path = Path(__file__).resolve().parents[1] / "config" / "settings.json"
        else:
            self.config_path = Path(config_path)
        self.config_path.parent.mkdir(parents=True, exist_ok=True)

    def load(self):
        if not self.config_path.exists():
            self.save(DEFAULT_SETTINGS)
            return DEFAULT_SETTINGS.copy()

        try:
            with self.config_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = DEFAULT_SETTINGS.copy()

        for key, value in DEFAULT_SETTINGS.items():
            data.setdefault(key, value)

        return data

    def save(self, settings):
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with self.config_path.open("w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4)
