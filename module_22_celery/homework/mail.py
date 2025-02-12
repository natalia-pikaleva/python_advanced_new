import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

from config import SMTP_HOST, SMTP_PORT, SMTP_PASSWORD, SMTP_USER
import logging

logger = logging.getLogger(__name__)

from celery import Celery

celery = Celery('app',
                broker='redis://localhost:6379/0',
                backend='redis://localhost:6379/0')


@celery.task
def send_email(receiver: str, filename: str, order_id: str = "", ):
    """
    Отправляет пользователю `receiver` письмо по заказу `order_id` с приложенным файлом `filename`
    Вы можете изменить логику работы данной функции
    """
    try:
        logger.info(f"Попытка отправить сообщение на адрес: {receiver}")
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            email = MIMEMultipart()
            email['Subject'] = f'Изображения. Заказ №{order_id}'
            email['From'] = SMTP_USER
            email['To'] = receiver

            logger.info(f"Subject: {email['Subject']}, From: {email['From']}, To: {email['To']}")

            with open(filename, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())

            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={filename}')
            email.attach(part)
            text = email.as_string()
            server.sendmail(SMTP_USER, receiver, text)
        logger.info(f"Email sent successfully to {receiver}")
    except Exception as e:
        logger.error(f"Error sending email to {receiver}: {e}")
    # finally:
    #     # Always cleanup the temporary file
    #     try:
    #         os.remove(filename)
    #         logger.info(f"Удален временный файл: {filename}")
    #     except Exception as e:
    #         logger.error(f"Не удалось удалить временный файл {filename}: {e}")
