FROM python:3.10-slim-buster

RUN apt-get update && apt-get install -y cron

COPY src /app
COPY requirements.txt /app
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p /videos-to-search
