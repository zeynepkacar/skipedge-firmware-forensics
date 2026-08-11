"""
Central logging configuration for the firmware forensics toolkit.
All layers import get_logger() from this module instead of using print().
"""
import logging
import os

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
LOG_FILE = os.path.join(LOG_DIR, "analysis.log")

os.makedirs(LOG_DIR, exist_ok=True)

_configured = False


def get_logger(name):
    """Returns a logger configured to write to both console and analysis.log."""
    global _configured

    if not _configured:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            handlers=[
                logging.FileHandler(LOG_FILE, encoding="utf-8"),
                logging.StreamHandler(),
            ],
        )
        _configured = True

    return logging.getLogger(name)