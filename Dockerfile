FROM python:3.11-slim

LABEL maintainer="andr.vldz@gmail.com"

WORKDIR /app

ARG BOT_TOKEN

ENV BOT_TOKEN=${BOT_TOKEN}

RUN curl -sSL https://install.python-poetry.org | python3 - && \
	ln -s /root/.local/bin/poetry /usr/local/bin/poetry

COPY pyproject.toml poetry.lock* /app/

RUN poetry config virtualenvs.create false && \
    poetry install --no-root --only main --no-interaction --no-ansi

COPY . /app

CMD ["poetry", "run", "python", "src/crc-bot/main.py"]