import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


def get_logger(name: str = __name__) -> logging.Logger:
    """
    Returns a configured logger instance with rotating file handler.

    Rotation policy:
        - Max 5 MB per log file
        - Keeps 3 backup files  →  15 MB total disk cap
        - Files: app.log  →  app.log.1  →  app.log.2  →  app.log.3 (then discarded)

    Usage:
        from logger import get_logger
        logger = get_logger(__name__)

        logger.info("Server started")
        logger.warning("Low memory")
        logger.error("Something went wrong")
        logger.debug("Debug details")
        logger.critical("Critical failure")
    """

    logger = logging.getLogger(name)

    # Avoid adding duplicate handlers if logger already configured
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    # ── Format ──────────────────────────────────────────────────────────────
    # Example output:
    # 2026-04-23 10:45:32 | INFO     | main.py | create_user() | line 42 | User created
    fmt = (
        "%(asctime)s | %(levelname)-8s | %(filename)s | %(funcName)s() "
        "| line %(lineno)d | %(message)s"
    )
    formatter = logging.Formatter(fmt, datefmt="%Y-%m-%d %H:%M:%S")

    # ── Console handler (stdout) ─────────────────────────────────────────────
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    # ── Rotating file handler (logs/app.log) ─────────────────────────────────
    # Max 5 MB per file, keeps only the last 3 backup files -> 15 MB total cap
    # Rotation order: app.log -> app.log.1 -> app.log.2 -> app.log.3 (oldest deleted)
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    file_handler = RotatingFileHandler(
        log_dir / "app.log",
        maxBytes=5 * 1024 * 1024,  # 5 MB per file
        backupCount=3,  # app.log + 3 backups = 4 files max
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    # Prevent log records from bubbling up to the root logger
    logger.propagate = False

    return logger
