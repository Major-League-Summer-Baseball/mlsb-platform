# -*- coding: utf-8 -*-
"""Holds a logger for the application."""
import os
import logging
import sys


def setupLogger() -> logging.Logger:
    """Setups the logger to use for the project

    Returns:
        logging.Logger: the project logger
    """
    level = os.environ.get("logging", "info")
    logger = logging.getLogger()
    handler = logging.StreamHandler(sys.stdout)
    if "debug" in level.lower():
        logger.setLevel(logging.DEBUG)
        handler.setLevel(logging.DEBUG)
    elif "info" in level.lower():
        logger.setLevel(logging.INFO)
        handler.setLevel(logging.INFO)
    elif "error" in level.lower():
        logger.setLevel(logging.ERROR)
        handler.setLevel(logging.ERROR)
    elif "warning" in level.lower():
        logger.setLevel(logging.WARNING)
        handler.setLevel(logging.WARNING)
    elif "error" in level.lower():
        logger.setLevel(logging.ERROR)
        handler.setLevel(logging.ERROR)
    elif "critical" in level.lower():
        logger.setLevel(logging.CRITICAL)
        handler.setLevel(logging.CRITICAL)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


LOGGER = setupLogger()
