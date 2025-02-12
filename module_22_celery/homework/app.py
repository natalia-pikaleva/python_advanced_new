from flask import Flask, request, jsonify
from celery import group
import logging
from celery_tasks import (blur_image_task, get_status, add_user_to_weekly_emails,
                          unsubscribe_user, subscriptions)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

app = Flask(__name__)


@app.route('/blur', methods=['POST'])
def blur():
    """Обрабатывает список изображений"""
    images = request.json.get('images')

    if images and isinstance(images, list):
        task_group = group(
            blur_image_task.s(image_path)
            for image_path in images
        )

        result = task_group.apply_async()
        result.save()

        return jsonify({'group_id': result.id}), 202
    else:
        return jsonify({'error': 'Missing or invalid images parameter'}), 400


@app.route('/status/<id>', methods=['GET'])
def get_status_by_id(id: str):
    """Если группа с таким ID существует, возвращает % выполненных задач"""
    result = get_status(id)

    if result:
        status = result.completed_count() / len(result)
        if status == 1.0:
            return jsonify({'status': 'Все изображения обработаны'}), 200
        else:
            return jsonify({'status': f'Обработано {status * 100}% изображений'}), 200
    else:
        return jsonify({'error': 'Invalid group_id'}), 404


@app.route('/subscribe', methods=['POST'])
def subscribe():
    """Подписывает пользователя на еженедельную рассылку."""
    email = request.json.get('email')

    if not email:
        return jsonify({'error': 'Invalid email'}), 400

    if '@' not in email:
        return jsonify({'error': 'Invalid email format'}), 400

    add_user_to_weekly_emails.delay(email)
    return jsonify({'result': 'Subscription completed successfully. You will receive weekly emails.'}), 201


@app.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    """Отменяет еженедельную рассылку пользователю"""
    email = request.json.get('email')
    if not email:
        return jsonify({'error': 'Invalid email'}), 400

    unsubscribe_user.delay(email)

    return jsonify({'result': 'Subscription uncompleted successfully.'}), 201


if __name__ == '__main__':
    app.run(debug=True)
