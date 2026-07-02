import subprocess
from pathlib import Path

from config.settings import APP_NAME, APP_VERSION, BUILDER_VERSION
from core.paths import PROJECT_ROOT, APP_LOG_FILE


class SystemInfoService:
    def __init__(self, app_state):
        self.app_state = app_state

    def get_git_branch(self):
        try:
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                cwd=PROJECT_ROOT,
                text=True,
                capture_output=True,
                check=False
            )
            return result.stdout.strip() or "Unknown"
        except Exception:
            return "Unavailable"

    def get_git_status_summary(self):
        try:
            result = subprocess.run(
                ["git", "status", "--short"],
                cwd=PROJECT_ROOT,
                text=True,
                capture_output=True,
                check=False
            )
            output = result.stdout.strip()
            return "Clean" if not output else "Changes pending"
        except Exception:
            return "Unavailable"

    def count_plugins(self):
        try:
            return len(list((PROJECT_ROOT / "src" / "plugins").glob("*_plugin.py")))
        except Exception:
            return 0

    def count_releases(self):
        releases_dir = PROJECT_ROOT / "releases"
        if not releases_dir.exists():
            return 0
        return len([p for p in releases_dir.iterdir() if p.is_dir()])

    def get_health_report(self):
        theme = self.app_state.config_manager.get("theme", "light")
        current_page = self.app_state.current_page

        return {
            "Application": APP_NAME,
            "Version": APP_VERSION,
            "Builder Version": BUILDER_VERSION,
            "Project Root": str(PROJECT_ROOT),
            "Current Page": current_page,
            "Theme": theme,
            "Git Branch": self.get_git_branch(),
            "Git Status": self.get_git_status_summary(),
            "Installed Plugins": self.count_plugins(),
            "Release Snapshots": self.count_releases(),
            "Log File": str(APP_LOG_FILE),
            "Health Status": "Healthy",
        }

    def format_health_report(self):
        report = self.get_health_report()
        lines = ["GH Workspace Manager - System Information & Health Center", ""]

        for key, value in report.items():
            lines.append(f"{key:.<24} {value}")

        return "\n".join(lines)
