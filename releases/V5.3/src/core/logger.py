import logging
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
