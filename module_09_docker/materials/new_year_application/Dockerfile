FROM python:3.7.9-slim-stretch

WORKDIR /app

RUN mkdir /app.py

COPY requirements.txt .

RUN python -m pip install -r requirements.txt

COPY . .

COPY ./templates ./templates

COPY ./static ./static

ENTRYPOINT ["python", "app.py"]