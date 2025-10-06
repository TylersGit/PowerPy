# PowerPy/__init__.py
import logging

# Top-level logger for the library
logger = logging.getLogger("PowerPy")

# Optional: provide a helper to let users quickly enable logging
def enable_logging(level=logging.INFO):
    """
    Enable logging for PowerPy.
    Users can also configure logging themselves instead of calling this.
    """
    # Only add handler if none exist to avoid double-logging
    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(level)




enable_logging(logging.DEBUG)

logger.debug("PowerPy initialized")