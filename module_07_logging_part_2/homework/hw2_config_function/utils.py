from typing import Union, Callable
from operator import sub, mul, truediv, add
import logging

utils_logger = logging.getLogger('utils_logger')
utils_logger.setLevel(logging.DEBUG)
utils_logger.propagate = False
custom_handler = logging.StreamHandler()
utils_logger.addHandler(custom_handler)
formatter = logging.Formatter(fmt="%(levelname)s | %(name)s %(asctime)s | %(lineno)s | %(message)s")
custom_handler.setFormatter(formatter)

OPERATORS = {
    '+': add,
    '-': sub,
    '*': mul,
    '/': truediv,
}

Numeric = Union[int, float]


def string_to_operator(value: str) -> Callable[[Numeric, Numeric], Numeric]:
    """
    Convert string to arithmetic function
    :param value: basic arithmetic function
    """
    utils_logger.info('Started string_to_operator')
    if not isinstance(value, str):
        utils_logger.error(f"Wrong operator type: {value}")
        return False

    if value not in OPERATORS:
        utils_logger.error(f"Wrong operator value: {value}")
        return False

    utils_logger.info(f'Successfully take operator {value}')
    return OPERATORS[value]
