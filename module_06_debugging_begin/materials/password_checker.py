import getpass
import hashlib
import logging
import re

logger = logging.getLogger("password_checker")


def input_and_check_password():
    logger.debug("Начало input_and_check_password")
    password: str = getpass.getpass()
    logger.debug(f"Пользователь ввел пароль")



    if not password:
        logger.warning("Вы ввели пустой пароль.")
        return False

    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@$%^&*()\-+=_]).{8,}$'

    if not re.search(pattern, password):
        logger.warning("Ваш пароль слабый. Хороший пароль должен быть минимум восемь символов, большие и маленькие буквы, "
                    "а также как минимум одна цифра и один символ из списка !@#$%^&*()-+=_')")

    try:
        hasher = hashlib.md5()
        logger.debug(f"Мы создали объект hasher {hasher!r}")

        hasher.update(password.encode("latin-1"))

        if hasher.hexdigest() == "098f6bcd4621d373cade4e832627b4f6":
            logger.debug(f"Проверяем корректность пароля")
            return True
    except ValueError as ex:
        logger.debug(f"Обрабатываем ошибку {ex}")
        logger.exception("Вы ввели некорректный символ ", exc_info=ex)

    return False


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logger.info("Вы пытаетесь аутентифицироваться в Skillbox")

    while True:
        logger.info("Введите количество попыток для входы в систему. Количество попыток может быть от 2 до 10")
        try:
            count_number: int = int(input())
            if 2 <= count_number <= 10:
                break

        except ValueError:
            logger.warning("Вы ввели некорректные данные. Количество попыток может быть от 2 до 10.")



    logger.info(f"У вас есть {count_number} попытки")


    while count_number > 0:
        if input_and_check_password():
            exit(0)
        count_number -= 1

    logger.error("Количество попыток закончилось!")
    exit(1)
