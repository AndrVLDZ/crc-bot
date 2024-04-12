FROM python:3.11-slim  as python-base

LABEL maintainer="andr.vldz@gmail.com"

ARG BOT_TOKEN

ENV BOT_TOKEN=${BOT_TOKEN} \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

FROM python-base as builder-base

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        build-essential

ENV POETRY_VERSION=1.8.2
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python


WORKDIR $PYSETUP_PATH
COPY pyproject.toml poetry.lock* /app/
RUN poetry install --no-root --only main --no-interaction --no-ansi


COPY --from=builder-base $POETRY_HOME $POETRY_HOME
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

COPY ./docker/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh


WORKDIR $PYSETUP_PATH
RUN poetry install


WORKDIR /app
COPY . /app

CMD ["poetry", "run", "python", "src/crc-bot/main.py"]