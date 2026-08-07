import logging
from pathlib import Path


LOG_DIR = Path("outputs")
LOG_DIR.mkdir(parents=True, exist_ok=True)


def setup_logger():

    logger = logging.getLogger("ECommerceAnalytics")

    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    # Console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # File
    file_handler = logging.FileHandler(
        LOG_DIR / "analytics.log",
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger