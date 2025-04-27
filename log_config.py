import logging
import logging.handlers
from pathlib import Path

def setup_logger(name="chat"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Create server-logs folder relative to this file
    log_dir = Path(__file__).parent / "server-logs"
    log_dir.mkdir(exist_ok=True)

    log_file = log_dir / "server.log"

    handler = logging.handlers.TimedRotatingFileHandler(
        log_file,
        when="midnight",
        backupCount=7
    )
    handler.setFormatter(logging.Formatter("[%(asctime)s] [%(name)s] %(message)s"))
    logger.addHandler(handler)
    return logger
