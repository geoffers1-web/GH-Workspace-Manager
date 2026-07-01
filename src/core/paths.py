from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"
DOCS_DIR = PROJECT_ROOT / "docs"
CONFIG_DIR = SRC_DIR / "config"
APP_CONFIG_DIR = PROJECT_ROOT / ".gh_workspace"
APP_CONFIG_FILE = APP_CONFIG_DIR / "gh_workspace_config.json"
