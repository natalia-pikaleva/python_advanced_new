import logging
import sys
from logging.handlers import TimedRotatingFileHandler


class LevelFileHandler(logging.Handler):
    def __init__(self):
        super().__init__()

    def emit(self, record: logging.LogRecord) -> None:
        message = self.format(record)
        level_name = record.levelname
        file_name = "calc_" + level_name.lower() + ".log"

        with open(file_name, "a") as f:
            f.write(message + '\n')


class ASCIIFilter(logging.Filter):
    def filter(self, record):
        message = record.getMessage()
        return message.isascii()


dict_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "base": {
            "format": "%(levelname)s | %(name)s | %(asctime)s | %(lineno)s | %(message)s"
        }
    },
    "filters": {
        "custom_filter": {
            "()": ASCIIFilter
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "base",
            "filters": ["custom_filter"]
        },
        "file": {
            "()": LevelFileHandler,
            "level": "DEBUG",
            "formatter": "base",
            "filters": ["custom_filter"]
        },
        "file_time_rotate": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "DEBUG",
            "formatter": "base",
            "filename": "utils.log",
            "when": "h",
            "interval": 10,
            "backupCount": 2,
            "filters": ["custom_filter"]
        }
    },
    "loggers": {
        "app_logger": {
            "level": "DEBUG",
            "handlers": ["file", "console"],
            "filters": ["custom_filter"]
        },
        "utils_logger": {
            "level": "INFO",
            "handlers": ["file_time_rotate", "console"],
            "filters": ["custom_filter"]
        }
    },
    # "root": {} # == "": {}
}
