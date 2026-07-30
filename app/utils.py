"""
Utility functions for the DEVFORGE Student Support AI Agent.
"""

import logging
import time


# Configure logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


def log_info(message: str) -> None:
    """
    Log an informational message.
    """
    logger.info(message)


def log_error(message: str) -> None:
    """
    Log an error message.
    """
    logger.error(message)


def current_timestamp() -> float:
    """
    Return current timestamp.
    """
    return time.time()


def response_time(start_time: float) -> float:
    """
    Calculate response time in seconds.
    """
    return round(time.time() - start_time, 3)


def clean_text(text: str) -> str:
    """
    Clean user input by removing extra spaces.
    """
    return " ".join(text.strip().split())


def is_empty(text: str) -> bool:
    """
    Check if user input is empty.
    """
    return len(clean_text(text)) == 0