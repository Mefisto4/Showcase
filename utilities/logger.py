"""
Contains logger setup.
"""

import logging

LOGGER_FILE_PATH = "reports/logger-logs.log"


def get_logger(name: str | None = None) -> logging.Logger:
    """
    Function to set file handler, generate log file and return logger instance.

    :param name: name for a logger
    :return: the logger instance
    """
    _logger = logging.getLogger(name or __name__)

    # Set main options
    logging_level = logging.DEBUG
    formatter = logging.Formatter(
        fmt="%(asctime)s :@: %(name)s :@: %(levelname)s :@: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )  # ' :@: ' - delimiter, 5 characters

    # File handler to move stdout to log file
    file_handler = logging.FileHandler(LOGGER_FILE_PATH, mode="a", encoding="utf-8")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging_level)

    # Add handlers
    _logger.handlers.clear()
    _logger.addHandler(file_handler)

    return _logger
