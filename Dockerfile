FROM python:3.10-slim

WORKDIR /code

ENV VIRTUAL_ENV=/code/src/venv \
    PATH="/code/src/venv/bin:${PATH}" \
    PYTHONPATH=${PYTHONPATH}:/code/src \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

COPY ./pyproject.toml /code/pyproject.toml
COPY ./poetry.lock /code/poetry.lock
COPY ./ch /code/ch

ARG POETRY_VERSION=1.7.1

RUN python3.10 -m venv --system-site-packages $VIRTUAL_ENV \
    && pip3 install poetry~=$POETRY_VERSION \
    && poetry install -vvv --no-interaction --no-root \
    && rm -rf /root/.cache/pypoetry

COPY ./src /code/src
