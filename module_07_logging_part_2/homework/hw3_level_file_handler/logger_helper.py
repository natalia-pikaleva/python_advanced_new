import logging
import sys


class LevelFileHandler(logging.Handler):
    def __init__(self, file_name="", mode='a'):
        super().__init__()
        self.file_name = file_name
        self.mode = mode

    def emit(self, record: logging.LogRecord) -> None:
        message = self.format(record)
        level_name = record.levelname
        file_name = "calc_" + level_name.lower() + ".log"

        with open(file_name, "a") as f:
            f.write(message + '\n')


def get_logger(name):
    logger = logging.getLogger(name)
    handler = LevelFileHandler()
    logger.addHandler(handler)
    formatter = logging.Formatter(fmt="%(levelname)s | %(name)s | %(asctime)s | %(lineno)s | %(message)s",
                                  datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    return logger
