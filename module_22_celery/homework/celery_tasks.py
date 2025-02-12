"""
В этом файле будут Celery-задачи
"""

from celery import Celery
import logging
from celery.schedules import crontab
from image import blur_image
from datetime import datetime
from mail import send_email
from bd import save_data_ib_bd, get_data_by_email

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

celery = Celery(
    'app',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

# Дополнительная конфигурация
celery.conf.update(
    result_expires=3600,
    enable_utc=True,
    timezone='UTC',
)

celery.conf.beat_schedule = {
    'send_weekly_emails': {
        'task': 'celery_tasks.process_weekly_emails',
        'schedule': crontab(day_of_week='mon', hour=9, minute=0),  # Каждый понедельник в 09.00
    },
}

subscriptions = {}


@celery.task
def blur_image_task(image_path):
    return blur_image(image_path)


def get_status(id: str):
    return celery.GroupResult.restore(id)


@celery.task
def add_user_to_weekly_emails(email: str):
    """Добавляет пользователя в еженедельную рассылку. Если пользователь уже есть, обновляет дату подписки."""

    logger.info(f"Старт функции add_user_to_weekly_emails")
    global subscriptions

    now = datetime.utcnow()

    if email in subscriptions:
        logger.info(f"email: {email}")
        subscriptions[email] = now
        logger.info(f"Пользователь {email} уже подписан, обновляем дату подписки.")
    else:
        subscriptions[email] = now
        logger.info(f"Подписываем пользователя {email} на еженедельную рассылку.")


@celery.task
def process_weekly_emails():
    """Проходит по списку подписок и отправляет письма тем, кому пора."""
    logger.info(f"Старт функции process_weekly_emails")
    global subscriptions
    now = datetime.utcnow()

    logger.info(f"Текущее время: {now}")
    logger.info(f"Список подписок: {subscriptions}")

    for email, subscription_date in list(subscriptions.items()):
        try:
            logger.info(f"Вызываем функцию send_email для {email}")
            id, filename = get_data_by_email(email)
            logger.info(f"Вызываем функцию get_data_by_email для {email}")
            logger.info(f"id: {id}, filename: {filename}")
            send_email.delay(receiver=email, filename=filename, order_id=id)
            subscriptions[email] = now
        except Exception as e:
            logger.error(f"Ошибка при отправке email на {email}: {e}")


@celery.task
def unsubscribe_user(email: str):
    """Удаляет пользователя из еженедельной рассылки."""
    global subscriptions
    try:
        subscriptions.pop(email, None)  # Безопасное удаление
        logger.info(f"Пользователь {email} отписан от рассылки.")
    except KeyError:
        logger.warning(f"Пользователь {email} не найден в списке подписок.")
    except Exception as e:
        logger.error(f"Ошибка при отписке пользователя {email}: {e}")


@celery.task
def send_email_after_blur(results, email):
    """
    Эта функция вызывается после завершения всех задач размытия.
    Она получает список имен файлов и вызывает send_email для каждого из них.
    """
    logger.info(f"send_email_after_blur called with results: {results} and email: {email}")

    for filename in results:
        send_email.delay(email, filename)  # Отправляем каждый файл на почту

    save_data_ib_bd(email=email, files_list=results)
    return True
