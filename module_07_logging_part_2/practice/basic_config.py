import logging
import logging.config
from logging_config import dict_config

logging.config.dictConfig(dict_config)

logger = logging.getLogger('module_logger')
logger.setLevel("DEBUG")
logger.debug("msg", extra={"very": "much"})

def main():
    logger.debug("Hi there!")



if __name__ == '__main__':
    main()