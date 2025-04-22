
import logging
from log_config import setup_logger
from pathlib import Path

def test_logger_creates_log_dir_and_handler(tmp_path, monkeypatch):
    # Override the default log directory with a temporary path
    monkeypatch.setattr("log_config.Path", lambda p="": tmp_path / "server-logs")

    logger = setup_logger("test_logger")

    log_dir = tmp_path / "server-logs"
    log_file = log_dir / "server.log"

    # Ensure log directory and log file were set up
    assert log_dir.exists()
    assert any(isinstance(h, logging.handlers.TimedRotatingFileHandler) for h in logger.handlers)
    assert logger.name == "test_logger"
    assert logger.level == logging.INFO
