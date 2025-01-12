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


dict_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "base": {
            "format": "%(levelname)s | %(name)s | %(asctime)s | %(lineno)s | %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "base"
        },
        "file": {
            "()": LevelFileHandler,
            "level": "DEBUG",
            "formatter": "base"
        }
    },
    "loggers": {
        "app_logger": {
            "level": "DEBUG",
            "handlers": ["file", "console"]
        },
        "utils_logger": {
            "level": "DEBUG",
            "handlers": ["file", "console"]
        }
    }
}
