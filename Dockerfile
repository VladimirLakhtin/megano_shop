FROM python:3.11

ENV PYTHONUNBUFFERED=1

WORKDIR /megano

COPY requirements.txt requirements.txt
COPY frontend-0.6.tar.gz frontend.tar.gz

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install frontend.tar.gz

COPY megano .

RUN python manage.py migrate
RUN python manage.py loaddata accounts/fixtures/users_data.json
RUN python manage.py loaddata catalog/fixtures/catalog_data.json
RUN python manage.py loaddata products/fixtures/products_data.json
RUN python manage.py loaddata orders/fixtures/orders_data.json
