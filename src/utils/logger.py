import logging
import os
import sys
from logging.handlers import RotatingFileHandler

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)


# --------- Custom Formatter with Colors for Console ---------
class ColorFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[41m",  # Red background
    }
    RESET = "\033[0m"

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.RESET)
        message = super().format(record)
        return f"{log_color}{message}{self.RESET}"


# --------- Formatters ---------
file_formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)-8s] [%(name)s:%(funcName)s:%(lineno)d] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

console_formatter = ColorFormatter(
    "[%(asctime)s] [%(levelname)-8s] [%(name)s] - %(message)s", datefmt="%H:%M:%S"
)

# --------- File Handler (rotating) ---------
file_handler = RotatingFileHandler(
    filename=os.path.join(LOG_DIR, "app.log"),
    maxBytes=5 * 1024 * 1024,  # 5 MB
    backupCount=5,
    encoding="utf-8",
)
file_handler.setFormatter(file_formatter)

# --------- Console Handler ---------
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(console_formatter)

# --------- Logger Setup ---------
logger = logging.getLogger("finance_manager")
logger.setLevel(logging.DEBUG)  # log everything, filter by handlers
logger.addHandler(file_handler)
logger.addHandler(console_handler)
