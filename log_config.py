import logging
import logging.handlers
import os
from pathlib import Path

def setup_logger(name="chat"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    log_dir = Path("LOG_DIR","server-logs")
    log_dir.mkdir(exist_ok=True)        # create folder if it doesn’t exist
    log_file = log_dir / "server.log"

    handler = logging.handlers.TimedRotatingFileHandler(
        log_file,
        when="midnight",
        backupCount=7
    )
    handler.setFormatter(logging.Formatter("[%(asctime)s] [%(name)s] %(message)s"))
    logger.addHandler(handler)
    return logger
