FROM python:3.10-slim

RUN mkdir /app

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends htop

COPY requirements.txt .

RUN python -m pip install -r requirements.txt

COPY app.py /app/

COPY templates /app/templates

COPY static /app/static

ENTRYPOINT ["python", "app.py"]