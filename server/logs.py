import logging
import sys
from typing import Any

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

# Create base logger
logger = logging.getLogger("server")
logger.setLevel(logging.INFO)


def get_logger(name: str) -> Any:
    """Get a logger with the given name, inheriting base configuration."""
    return logger.getChild(name)
