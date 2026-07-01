from pathlib import Path

files = {
    "src/config/settings.py": '''APP_NAME = "GH Workspace Manager"
APP_VERSION = "4.5"
WINDOW_TITLE = f"{APP_NAME} V{APP_VERSION}"

DEFAULT_WINDOW_WIDTH = 1100
DEFAULT_WINDOW_HEIGHT = 700

CONFIG_FILE_NAME = "gh_workspace_config.json"
LOG_FILE_NAME = "gh_workspace.log"
''',

    "src/core/paths.py": '''from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"
DOCS_DIR = PROJECT_ROOT / "docs"
CONFIG_DIR = SRC_DIR / "config"

APP_DATA_DIR = PROJECT_ROOT / ".gh_workspace"
APP_CONFIG_FILE = APP_DATA_DIR / "gh_workspace_config.json"
APP_LOG_FILE = APP_DATA_DIR / "gh_workspace.log"
''',

    "src/core/logger.py": '''import logging
from core.paths import APP_LOG_FILE


def setup_logger():
    APP_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("GHWorkspaceManager")
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_handler = logging.FileHandler(APP_LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


app_logger = setup_logger()
''',

    "src/core/app_state.py": '''from config.config_manager import ConfigManager
from core.paths import APP_CONFIG_FILE
from core.logger import app_logger


class AppState:
    def __init__(self):
        self.logger = app_logger
        self.logger.info("Starting GH Workspace Manager")

        self.config_manager = ConfigManager(APP_CONFIG_FILE)
        self.current_page = self.config_manager.get("last_page", "dashboard")
        self.status_message = "Ready"

    def set_current_page(self, page_name):
        self.current_page = page_name
        self.config_manager.set("last_page", page_name)
        self.logger.info(f"Page changed to: {page_name}")
''',

    "src/services/git_service.py": '''import subprocess
from pathlib import Path
from core.logger import app_logger


class GitService:
    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
        self.logger = app_logger

    def run_git_command(self, args):
        command = "git " + " ".join(args)
        self.logger.info(f"Running command: {command}")

        try:
            result = subprocess.run(
                ["git"] + args,
                cwd=self.repo_path,
                text=True,
                capture_output=True,
                check=False
            )

            output = result.stdout.strip() or result.stderr.strip()

            if result.returncode == 0:
                self.logger.info(f"Command completed: {command}")
            else:
                self.logger.warning(f"Command warning/error: {output}")

            return output

        except Exception as error:
            self.logger.exception("Git command failed")
            return f"Git error: {error}"

    def status(self):
        return self.run_git_command(["status"])

    def log(self):
        return self.run_git_command(["log", "--oneline", "-10"])
''',

    "src/gui/pages/dashboard_page.py": '''import tkinter as tk
from core.paths import APP_LOG_FILE


class DashboardPage(tk.Frame):
    def __init__(self, parent, app_state):
        super().__init__(parent)
        self.app_state = app_state

        title = tk.Label(
            self,
            text="Dashboard & Workspace Health",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=20)

        message = tk.Label(
            self,
            text="GH Workspace Manager professional modular architecture is running.",
            font=("Arial", 12)
        )
        message.pack(pady=10)

        log_info = tk.Label(
            self,
            text=f"Log file: {APP_LOG_FILE}",
            font=("Arial", 10)
        )
        log_info.pack(pady=10)
'''
}


def main():
    for path, content in files.items():
        file_path = Path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        print(f"Updated: {file_path}")

    print("\\nV4.5 Logging Framework created successfully.")


if __name__ == "__main__":
    main()
