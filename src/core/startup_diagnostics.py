import platform
import sys
from pathlib import Path

from core.logger import app_logger


def run_startup_diagnostics():
    """
    Record basic startup diagnostics in the application log.
    """
    project_root = Path.cwd()

    app_logger.info("Startup diagnostics beginning")
    app_logger.info("Python version: %s", sys.version.split()[0])
    app_logger.info("Platform: %s", platform.platform())
    app_logger.info("Project root: %s", project_root)

    required_directories = [
        project_root / "src",
        project_root / "data",
        project_root / "logs",
    ]

    for directory in required_directories:
        if directory.exists():
            app_logger.info("Directory check passed: %s", directory)
        else:
            app_logger.warning("Directory missing: %s", directory)

    app_logger.info("Startup diagnostics complete")
