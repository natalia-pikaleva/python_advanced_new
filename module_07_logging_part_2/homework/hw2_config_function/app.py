import sys
from utils import string_to_operator
import logging
import logging.config

logging.basicConfig(level = "DEBUG")
app_logger = logging.getLogger('app_logger')
app_logger.propagate = False
custom_handler = logging.StreamHandler()
app_logger.addHandler(custom_handler)
formatter = logging.Formatter(fmt="%(levelname)s | %(name)s | %(asctime)s | %(lineno)s | %(message)s")
custom_handler.setFormatter(formatter)


def calc(args):
    app_logger.debug(f'Starting calc')
    app_logger.debug(f'Arguments: {args}')

    try:
        num_1 = args[0]
        operator = args[1]
        num_2 = args[2]
    except Exception as ex:
        app_logger.error(f'Invalid arguments {args}: {ex}')
        return True

    try:
        num_1 = float(num_1)
    except ValueError as e:
        app_logger.error(f'Error while converting number 1: {e}')

    try:
        num_2 = float(num_2)
    except ValueError as e:
        app_logger.error(f'Error while converting number 2: {e}')

    try:
        operator_func = string_to_operator(operator)
    except Exception as ex:
        app_logger.error(f'Invalid operetor: {ex}')
        return True

    try:
        result = operator_func(num_1, num_2)

        if not result:
            app_logger.error("Can't make operation")
            return True



        print("Result: ", result)
        print(f"{num_1} {operator} {num_2} = {result}")
        app_logger.debug(f"Result: {num_1} {operator} {num_2} = {result}")
    except Exception as ex:
        app_logger.error(f"Can't make operation: {ex}")


if __name__ == '__main__':
    # calc(sys.argv[1:])

    calc('2+3')
    calc('2/0')
    calc(523)
    calc("523")
