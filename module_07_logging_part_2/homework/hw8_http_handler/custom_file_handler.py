import logging
# import sys
# from logging.handlers import TimedRotatingFileHandler
import requests
import json
from logging.handlers import HTTPHandler

class CustomHTTPHandler(HTTPHandler):
    def emit(self, record):
        try:
            msg = self.format(record)
            headers = {'Content-Type': 'application/json'}
            requests.post(f'http://{self.host}{self.url}', data=msg, headers=headers)
        except Exception:
            self.handleError(record)

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "level": record.levelname,
            "name": record.name,
            "asctime": self.formatTime(record),
            "lineno": record.lineno,
            "message": record.getMessage()
        }
        return json.dumps(log_entry)


class CustomFilter(logging.Filter):
    def filter(self, record):
        message = record.getMessage()
        return all(ord(char) < 128 for char in message)


dict_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "base": {
            "format": "%(levelname)s | %(name)s | %(asctime)s | %(lineno)s | %(message)s"
        },
        "json": {
            "()": JsonFormatter
        }
    },
    "filters": {
        "custom_filter": {
            "()": CustomFilter
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "base",
            "filters": ["custom_filter"]
        },
        # "file": {
        #     "()": LevelFileHandler,
        #     "level": "DEBUG",
        #     "formatter": "base",
        #     "filters": ["custom_filter"]
        # },
        "file_time_rotate": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "DEBUG",
            "formatter": "base",
            "filename": "utils.log",
            "when": "h",
            "interval": 10,
            "backupCount": 2,
            "filters": ["custom_filter"]
        },
        "http_handler": {
            "()": CustomHTTPHandler,
            "host": '127.0.0.1:3000',
            "url": '/log',
            "method": 'POST',
            "level": 'DEBUG',
            "formatter": "json"
        }
    },
    "loggers": {
        "app_logger": {
            "level": "DEBUG",
            "handlers": ["console", "http_handler"],
            "filters": ["custom_filter"]
        },
        "utils_logger": {
            "level": "DEBUG",
            "handlers": ["console", "http_handler"],
            "filters": ["custom_filter"]
        }
    }
}
