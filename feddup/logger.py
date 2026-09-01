"""
Fed-Dup Logging Configuration
"""

import logging
import sys


def get_logger(name: str) -> logging.Logger:
    """Return a configured logger that writes to stdout.

    The logger is idempotent: calling this multiple times with the same name
    will not duplicate handlers.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )

    if not logger.handlers:
        logger.addHandler(handler)

    logger.propagate = False
    return logger
