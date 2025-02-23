FROM python:3.10-slim

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все остальные файлы
COPY . .

# Указываем порт для приложения
EXPOSE 5000

# Запускаем приложение с gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "3", "--worker-class", "sync", "--timeout", "60", "app.__init__:app"]