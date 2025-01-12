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
# TODO Самое простое решение использовать тот же configparser:
#
# import configparser
# import json
#
# config_object = configparser.RawConfigParser()  # or use interpolation=None for just ConfigParser
# with open("logging_conf.ini","r") as file:
#     config_object.read_file(file)
#     output_dict = {s: dict(config_object.items(s)) for s in config_object.sections()}
# print("Dictionary config:\n", json.dumps(output_dict, indent=4))