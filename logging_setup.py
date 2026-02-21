# logging_config.py
import logging
from pathlib import Path

LOG_FILE = "log.txt"

def setup_logging():
    log_path = Path(LOG_FILE)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.FileHandler(log_path, mode="a"),  # append mode
            # logging.StreamHandler()  # optional: also print to console
        ]
    )