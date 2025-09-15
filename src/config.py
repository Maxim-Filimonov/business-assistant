from __future__ import annotations

import logging
from logging.config import dictConfig


def configure_logging(log_file: str = "routing.log") -> None:
    """Configure application logging with JSON formatting and rotation."""
    dictConfig(
        {
            "version": 1,
            "formatters": {
                "json": {
                    "format": '{"time":"%(asctime)s","level":"%(levelname)s","message":"%(message)s"}',
                    "datefmt": "%Y-%m-%dT%H:%M:%S",
                }
            },
            "handlers": {
                "file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "formatter": "json",
                    "filename": log_file,
                    "maxBytes": 1_000_000,
                    "backupCount": 5,
                }
            },
            "root": {
                "level": "INFO",
                "handlers": ["file"],
            },
        }
    )


# Configure on import
configure_logging()
