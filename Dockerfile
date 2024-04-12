FROM python:3.11-slim

LABEL maintainer="andr.vldz@gmail.com"

WORKDIR /app

ARG BOT_TOKEN

ENV BOT_TOKEN=${BOT_TOKEN} \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on

COPY requirements.txt .

RUN pip install -r requirements.txt
RUN pip list

COPY . .

CMD ["python", "src/crc-bot/main.py"]