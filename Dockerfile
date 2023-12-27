FROM python:3.11

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir -p /home/app

ENV HOME=/home/app
ENV APP_HOME=/home/app/megano
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/mediafiles
WORKDIR $APP_HOME

COPY pyproject.toml .
COPY poetry.lock .

COPY diploma-frontend-0.6/frontend/static $APP_HOME/staticfiles
COPY megano/media $APP_HOME/mediafiles

COPY frontend-0.6.tar.gz frontend.tar.gz
RUN pip install frontend.tar.gz

RUN pip install poetry
RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi --no-root

COPY megano .
