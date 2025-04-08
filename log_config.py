import logging
import logging.handlers

def setup_logger(name="chat"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    handler = logging.handlers.TimedRotatingFileHandler("server.log", when="midnight", backupCount=7)
    handler.setFormatter(logging.Formatter("[%(asctime)s] [%(name)s] %(message)s"))
    logger.addHandler(handler)
    return logger
