# -*- coding: utf-8 -*-
"""Holds a logger for the application."""
from os import environ
from logging import getLogger, StreamHandler, Formatter, DEBUG, INFO, \
    ERROR, WARNING, CRITICAL, Logger
import sys


def setupLogger() -> Logger:
    """Setups the logger to use for the project

    Returns:
        logging.Logger: the project logger
    """
    level = environ.get("logging", "info")
    logger = getLogger()
    handler = StreamHandler(sys.stdout)
    if "debug" in level.lower():
        logger.setLevel(DEBUG)
        handler.setLevel(DEBUG)
    elif "info" in level.lower():
        logger.setLevel(INFO)
        handler.setLevel(INFO)
    elif "error" in level.lower():
        logger.setLevel(ERROR)
        handler.setLevel(ERROR)
    elif "warning" in level.lower():
        logger.setLevel(WARNING)
        handler.setLevel(WARNING)
    elif "error" in level.lower():
        logger.setLevel(ERROR)
        handler.setLevel(ERROR)
    elif "critical" in level.lower():
        logger.setLevel(CRITICAL)
        handler.setLevel(CRITICAL)
    formatter = Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


LOGGER = setupLogger()
