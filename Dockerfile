FROM python:3.11.8-alpine3.19

LABEL maintainer="andr.vldz@gmail.com"

WORKDIR /app

ENV BOT_TOCKEN = ${BOT_TOCKEN}

RUN apk add --update --no-cache curl && \
	curl -sSL https://install.python-poetry.org | python3 - && \
	ln -s /root/.local/bin/poetry /usr/local/bin/poetry

COPY pyproject.toml poetry.lock* /app/

RUN apk add --update --no-caсhe --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev && \
    apk del .tmp-build-deps

COPY . /app

VOLUME /app/data

CMD ["python", "src/crc-bot/main.py"]