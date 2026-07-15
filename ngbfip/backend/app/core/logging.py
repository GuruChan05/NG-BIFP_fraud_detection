"""Logging configuration and utilities."""
import logging
import logging.handlers
import sys
from app.core.config import settings

# Create logger
logger = logging.getLogger("ng-bifp")
logger.setLevel(getattr(logging, settings.LOG_LEVEL))

# Create logs directory if it doesn't exist
import os
os.makedirs(os.path.dirname(settings.LOG_FILE), exist_ok=True)

# Console Handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(getattr(logging, settings.LOG_LEVEL))
console_formatter = logging.Formatter(
    '[%(asctime)s] %(name)s - %(levelname)s - %(message)s'
)
console_handler.setFormatter(console_formatter)

# File Handler
file_handler = logging.handlers.RotatingFileHandler(
    settings.LOG_FILE,
    maxBytes=10485760,  # 10MB
    backupCount=10
)
file_handler.setLevel(getattr(logging, settings.LOG_LEVEL))
file_formatter = logging.Formatter(
    '[%(asctime)s] %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
)
file_handler.setFormatter(file_formatter)

# Add handlers to logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)
