import logging
import sys


class CustomStreamHandler(logging.Handler):

    def __init__(self, stream=None):
        if stream is None:
            stream = sys.stderr
        super().__init__()
        self.stream = stream

    def emit(self, record):
        msg = self.format(record)
        self.stream.write(msg + '\n')
        self.stream.flush()

dict_config = {
    "version": 1,
    "disable_existing_logger": False,
    "formatters": {
        "base": {
            "format": "%(levelname)s | %(name)s | %(message)s"
        }
    },
    "handlers": {
        "console": {
            "()": CustomStreamHandler,
            "level": "DEBUG",
            "formatter": "base",
        },
        "file": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "base",
            "filename": "logfile.log",
            "mode": "a"
        }
    },
    "loggers": {
        "module_logger": {
            "level": "DEBUG",
            "handlers": ["file", "console"],
            # "propagate": False
        }
    },

    # "filters": {},
    # "root": {}
}