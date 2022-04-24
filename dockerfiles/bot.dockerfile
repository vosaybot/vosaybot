FROM python:alpine as base

ENV PYTHONPATH /bot
ENV POETRY_VIRTUALENVS_CREATE false

RUN apk add --update --no-cache build-base gcc make musl-dev libffi-dev \
    postgresql-dev python3-dev

WORKDIR /bot/

RUN pip install --upgrade pip && pip install poetry psycopg2

COPY poetry.lock pyproject.toml alembic.ini /bot/

FROM base AS development
RUN pip install debugpy && poetry install
COPY src /bot/

FROM base AS production
RUN poetry install --no-dev
COPY src /bot/
