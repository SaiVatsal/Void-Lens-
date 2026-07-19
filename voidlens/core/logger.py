"""
VoidLens logger — daily rotating file logger with separate streams.

Outputs:
    logs/scan.log    — general scan activity
    logs/errors.log  — errors and exceptions
    logs/debug.log   — verbose debug output
"""

from __future__ import annotations

import logging
import sys
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path


def setup_logger(
    log_dir: str | Path = "logs",
    verbose: bool = False,
) -> logging.Logger:
    """
    Configure the VoidLens logger with rotating file handlers.

    Args:
        log_dir: Directory for log files.
        verbose: If True, also output debug-level to console.

    Returns:
        Configured root logger for 'voidlens'.
    """
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("voidlens")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # scan.log — INFO and above
    scan_handler = TimedRotatingFileHandler(
        log_path / "scan.log", when="midnight", backupCount=30, encoding="utf-8"
    )
    scan_handler.setLevel(logging.INFO)
    scan_handler.setFormatter(fmt)
    logger.addHandler(scan_handler)

    # errors.log — WARNING and above
    error_handler = TimedRotatingFileHandler(
        log_path / "errors.log", when="midnight", backupCount=30, encoding="utf-8"
    )
    error_handler.setLevel(logging.WARNING)
    error_handler.setFormatter(fmt)
    logger.addHandler(error_handler)

    # debug.log — all levels
    debug_handler = TimedRotatingFileHandler(
        log_path / "debug.log", when="midnight", backupCount=7, encoding="utf-8"
    )
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(fmt)
    logger.addHandler(debug_handler)

    # Console — only in verbose mode, minimal output
    if verbose:
        console = logging.StreamHandler(sys.stderr)
        console.setLevel(logging.DEBUG)
        console.setFormatter(logging.Formatter("%(levelname)-8s %(message)s"))
        logger.addHandler(console)

    return logger
