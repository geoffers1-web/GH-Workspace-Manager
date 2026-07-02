from pathlib import Path
import importlib.util


class SettingsService:
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.settings_file = project_root / "src" / "config" / "settings.py"

    def load(self):
        defaults = {
            "APP_NAME": "GH Workspace Manager",
            "APP_VERSION": "Unknown",
            "APP_RELEASE": "VUnknown",
            "BUILDER_VERSION": "3.0",
        }

        if not self.settings_file.exists():
            return defaults

        try:
            spec = importlib.util.spec_from_file_location("settings", self.settings_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            app_version = getattr(module, "APP_VERSION", defaults["APP_VERSION"])

            return {
                "APP_NAME": getattr(module, "APP_NAME", defaults["APP_NAME"]),
                "APP_VERSION": app_version,
                "APP_RELEASE": getattr(module, "APP_RELEASE", f"V{app_version}"),
                "BUILDER_VERSION": getattr(module, "BUILDER_VERSION", defaults["BUILDER_VERSION"]),
            }
        except Exception as error:
            print(f"Could not load settings: {error}")
            return defaults
