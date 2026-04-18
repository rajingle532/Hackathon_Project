"""
Agentic Service — Structured Logging
=====================================
Provides a configured logger for the entire service.
"""

import logging
import sys
from config import settings


def setup_logger(name: str = "agentic") -> logging.Logger:
    """Create and configure a logger instance."""

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logger.level)

    formatter = logging.Formatter(
        fmt="%(asctime)s │ %(levelname)-7s │ %(name)-18s │ %(message)s",
        datefmt="%H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


# Default logger — import this in other modules
log = setup_logger()
