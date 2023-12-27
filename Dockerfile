FROM python:3.11

ENV PYTHONUNBUFFERED=1

WORKDIR /megano

COPY requirements.txt requirements.txt
COPY frontend-0.6.tar.gz frontend.tar.gz

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install frontend.tar.gz

COPY megano .
