import json
import logging
import os

from flask import Flask

app = Flask(__name__)
logger = logging.getLogger("account_book")

current_dir = os.path.dirname(os.path.abspath(__file__))
fixtures_dir = os.path.join(current_dir, "fixtures")

departments = {"IT": "it_dept", "PROD": "production_dept"}


@app.route("/account/<department>/<int:account_number>/")
def sort_endpoint(department: str, account_number: int):
    logging.debug("Успешно вошли в endpoint")

    dept_directory_name = departments.get(department)
    logging.debug(f"Получили название директории dept_directory_name {dept_directory_name}")

    if dept_directory_name is None:
        return "Department not found", 404

    full_department_path = os.path.join(fixtures_dir, dept_directory_name)
    logging.debug(f"Получили ссылку на директорию: {full_department_path}")

    account_data_file = os.path.join(full_department_path, f"{account_number}.json")
    logging.debug(f"Получили ссылку на файл: {account_data_file}")

    try:
        with open(account_data_file, "r", encoding='utf8') as fi:
            logging.debug(f"Открыли файл")
            account_data_txt = fi.read()
            logging.debug(f"Прочитали файл")

        try:
            account_data_json = json.loads(account_data_txt)
            logging.debug(f"Получили данные в виде json файла")

            name, birth_date = account_data_json["name"], account_data_json["birth_date"]

            if not name:
                logger.warning(f'В анкете сотрудника: {account_data_file} отсуствует имя')
                return f'В анкете сотрудника отсуствует имя'

            if not birth_date:
                logger.warning(f'В анкете сотрудника: {account_data_file} отсуствует дата рождения')
                return f'В анкете сотрудника {name} отсутсвует дата рождения'


            logging.debug(f"Получили из файла name: {name}, birth_date: {birth_date}")

            try:
                day, month, year = birth_date.split(".")
            except Exception as ex:
                logger.error(f"Ошибка в дате рождения в файле {account_data_file}, отсутствует день, месяц или год")
                return f'Невозможно предоставить информацию по данному сотруднику, так дата рождения в анкете прописана некорректно'

            try:
                day = int(day)
                month = int(month)
                year = int(year)
                if not 1 <= int(day) <= 31 or not 1 <= int(month) <= 12 or year > 2025:
                    logger.warning(f'В анкете сотрудника: {account_data_file} некорректно указана дата рождения: {birth_date}, день, месяц или год находятся вне допустимых диапазонов')
                    return f'В анкете данного сотрудника неверно указана дата рождения, необходимо исправить данные'

                return f"{name} was born on {day:02d}.{month:02d}"
            except Exception as ex:
                logger.warning(f'В анкете сотрудника: {account_data_file} некорректно указана дата рождения: {birth_date}, день или месяц не являются целыми числами')
                return f'В анкете данного сотрудника неверно указана дата рождения, необходимо исправить данные'
        except Exception as ex:
            logger.error(f"Ошибка при форматировании файла {account_data_file}: {ex}")
            return f'Невозможно предоставить информацию по данному сотруднику, так как файл с анкетой заполнен неверно'
    except FileNotFoundError:
        logger.error(f"Ошибка чтения файла {account_data_file}, возможно такого файла не существует")
        return f'Невозможно предоставить информацию по данному сотруднику, так как файл с анкетой отсутствует или поврежден'

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logger.info("Started account server")
    app.run(debug=True)
