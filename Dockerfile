FROM ubuntu:24.04

LABEL maintainer="andr.vldz@gmail.com"

WORKDIR /app

ENV BOT_TOCKEN=${BOT_TOCKEN}

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3.11 \
    python3.11-distutils \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3.11-venv \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 - && \
	ln -s /root/.local/bin/poetry /usr/local/bin/poetry

COPY pyproject.toml poetry.lock* /app/

RUN poetry config virtualenvs.create false && \
    poetry install --no-root --only main

COPY . /app

CMD ["python", "src/crc-bot/main.py"]