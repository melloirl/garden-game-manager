import logging
import os
from logging.handlers import RotatingFileHandler

LOG_DIR = os.getenv("LOG_DIR") or "/var/log/ggm"


class BotLogger:
    def __init__(
        self, name, log_level=logging.INFO, log_file_path=LOG_DIR, write_to_console=True
    ):
        self.log_file_path = log_file_path
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)

        # Ensure logs directory exists
        os.makedirs(self.log_file_path, exist_ok=True)

        # Define the format once for all handlers
        formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")

        # File Handler with rotation
        try:
            file_handler = RotatingFileHandler(
                filename=os.path.join(self.log_file_path, f"{name}.log"),
                maxBytes=5 * 1024 * 1024,
                backupCount=5,
            )
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        except Exception as e:
            print(f"Failed to create file handler: {e}")
            # No file handler will be added if this fails

        # Console Handler (stdout)
        if write_to_console:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)
