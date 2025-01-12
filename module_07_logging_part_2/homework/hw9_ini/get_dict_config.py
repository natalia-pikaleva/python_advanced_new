import configparser
from pprint import pprint

config = configparser.ConfigParser(interpolation=None)

config.read('logging_conf.ini')

dict_config = {
    'loggers': {},
    'handlers': {},
    'formatters': {}
}

if 'loggers' in config:
    for logger in config.sections():
        if logger.startswith('logger_'):
            dict_config['loggers'][logger[7:]] = dict(config.items(logger))

if 'handlers' in config:
    for handler in config.sections():
        if handler.startswith('handler_'):
            dict_config['handlers'][handler[8:]] = dict(config.items(handler))

if 'formatters' in config:
    for formatter in config.sections():
        if formatter.startswith('formatter_'):
            dict_config['formatters'][formatter[10:]] = dict(config.items(formatter))

for logger, value in dict_config['loggers'].items():
    dict_config['loggers'][logger]['handlers'] = value['handlers'].split(',')

print("Структурированный словарь из ini-файла:")
pprint(dict_config)
