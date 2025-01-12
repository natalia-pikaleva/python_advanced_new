dict_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "formatter_fileFormatter": {
            "format":" %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%S%Z"
        },
        "formatter_consoleFormatter": {
            "format": "%(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%S%Z"
        }
    },

    "handlers": {
        "handler_consoleHandler":{
            "class": "StreamHandler",
            "level": "WARNING",
            "formatter": "formatter_consoleFormatter",
            "args": "(sys.stdout,)"
        },
        "handler_fileHandler": {
            "class": "FileHandler",
            "level": "DEBUG",
            "formatter": "formatter_fileFormatter",
            "args": "('logfile.log',)"
        }
    },

    "loggers": {
        "root": {
            "level": "DEBUG",
            "handlers": ["handler_consoleHandler"]
        },
        "appLogger": {
            "level": "DEBUG",
            "handlers": ["handler_consoleHandler", "handler_fileHandler"],
            "qualname": "appLogger",
            "propagate": False
        }
    }
}