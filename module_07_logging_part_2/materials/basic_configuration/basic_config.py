import logging

root_logger = logging.getLogger()
logging.basicConfig()

module_logger = logging.getLogger('module_logger')
module_logger.propagate = False

submodule_logger = logging.getLogger('module_logger.submodule_logger')
submodule_logger.setLevel('DEBUG')
submodule_logger.propagate = True

custom_handler = logging.StreamHandler()
module_logger.addHandler(custom_handler)
formatter = logging.Formatter(fmt="%(levelname)s | %(name)s | %(message)s")
custom_handler.setFormatter(formatter)

file_handler = logging.FileHandler('applog.log', mode='a')
file_handler.setFormatter(formatter)
module_logger.addHandler(file_handler)

# Логгер sub_1
sub_1_logger = logging.getLogger('sub_1')
sub_1_logger.setLevel(logging.INFO)
sub_1_logger.propagate = True

# Логгер sub_2
sub_2_logger = logging.getLogger('sub_2')
sub_2_logger.propagate = False

# Логгер sub_sub_1
sub_sub_1_logger = logging.getLogger('sub_2.sub_sub_1')
sub_sub_1_logger.setLevel(logging.DEBUG)

# Обработчики
formatter = logging.Formatter(fmt="%(name)s || %(levelname)s || %(message)s || %(filename)s.%(funcName)s:%(lineno)s")

# Обработчик для sub_1
new_handler_sub_1 = logging.StreamHandler()
new_handler_sub_1.setLevel(logging.DEBUG)
new_handler_sub_1.setFormatter(formatter)
sub_1_logger.addHandler(new_handler_sub_1)

# Обработчик для sub_2
new_handler_sub_2 = logging.StreamHandler()
new_handler_sub_2.setLevel(logging.DEBUG)
new_handler_sub_2.setFormatter(formatter)
sub_2_logger.addHandler(new_handler_sub_2)

# Обработчик для root_logger
new_handler_root = logging.StreamHandler()
new_handler_root.setLevel(logging.DEBUG)
new_handler_root.setFormatter(formatter)
root_logger.addHandler(new_handler_root)


def main():
    print("Root logger:")
    print(root_logger.handlers)

    print("Submodule logger:")
    print(submodule_logger.handlers)

    print("Module logger:")
    print(module_logger.handlers)

    submodule_logger.debug("Hi there!")

    print('*' * 50)
    print(sub_1_logger, sub_1_logger.parent)
    print(sub_1_logger.handlers)

    print(sub_2_logger, sub_2_logger.parent)
    print(sub_2_logger.handlers)

    print(sub_sub_1_logger, sub_sub_1_logger.parent)
    print(sub_sub_1_logger.handlers)
    sub_1_logger.info('Какое-то сообщение')
    sub_2_logger.warning('Второе сообщение')
    sub_sub_1_logger.info('Еще какое-то сообщение')

    root_logger.warning('Корневое сообщение')


if __name__ == '__main__':
    main()
