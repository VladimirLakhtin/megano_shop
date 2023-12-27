FROM python:3.11

ENV PYTHONUNBUFFERED=1

WORKDIR /megano

COPY pyproject.toml .
COPY poetry.lock .
COPY frontend-0.6.tar.gz frontend.tar.gz

RUN pip install frontend.tar.gz
RUN pip install poetry
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi --no-root

COPY megano .
