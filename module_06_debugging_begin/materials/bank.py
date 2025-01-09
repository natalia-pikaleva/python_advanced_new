import csv
from typing import Optional

from flask import Flask
from werkzeug.exceptions import InternalServerError
import logging

app = Flask(__name__)
logger = logging.getLogger("divider")

@app.route("/bank_api/<branch>/<int:person_id>")
def bank_api(branch: str, person_id: int):
    logging.debug('Получаем данные из строки url')

    branch_card_file_name = f"./bank_data/{branch}.csv"
    logging.debug(f'Ссылка на файл получена: {branch_card_file_name}')

    logging.debug(f'Открываем файл: {branch_card_file_name}')
    with open(branch_card_file_name, "r", encoding='utf8') as fi:
        logging.debug(f'Файл: {branch_card_file_name} открыт')

        csv_reader = csv.DictReader(fi, delimiter=",")
        logging.debug(f'Получили данные файла в виде словаря csv_reader, ищем id {person_id}')

        for record in csv_reader:

            if int(record["id"]) == person_id:
                logging.debug(f'Нужный id найден')
                return record["name"]
        else:
            logging.debug(f'Нужный id не найден')
            return "Person not found", 404


@app.errorhandler(InternalServerError)
def handle_exception(e: InternalServerError):
    original: Optional[Exception] = getattr(e, "original_exception", None)

    if isinstance(original, FileNotFoundError):
        logger.exception("File not found", exc_info=e)
        # with open("invalid_error.log", "a") as fo:
        #     fo.write(
        #             f"Tried to access {original.filename}. Exception info: {original.strerror}\n"
        #     )
    elif isinstance(original, OSError):
        logger.exception("OSError", exc_info=e)
        # with open("invalid_error.log", "a") as fo:
        #     fo.write(f"Unable to access a card. Exception info: {original.strerror}\n")

    return "Internal server error", 500


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.info('Started bank server')
    app.run()
