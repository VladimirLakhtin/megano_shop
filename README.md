[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python&logoColor=blue)](https://www.python.org/downloads/release/python-3110/)
![Django 3.0](https://img.shields.io/badge/Django-4.2-red?style=for-the-badge&logo=django&logoColor=red)

# Django REST API shop
Django-ecommerce is an open-source ecommerce platform built on the Django Web Framework.
## Features Included
- Custom user model
- Authentication system
- Custom products filter 
- Shopping Cart
- Order Management
- Much more...

## Installation

**1. Сlone Repository**
```sh
git clone https://github.com/VladimirLakhtin/megano_shop

```
**2. Setup Virtualenv & Install Packages**
```sh
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
**3. Install frontend app**
```sh
pip install frontend-0.6.tar.gz

```
**4. Migrate & load fixtures**
```sh
python manage.py migrate
python manage.py loaddatautf8 accounts/fixtures/users_data.json
python manage.py loaddatautf8 catalog/fixtures/catalog_data.json
python manage.py loaddatautf8 products/fixtures/products_data.json
python manage.py loaddatautf8 orders/fixtures/orders_data.json
```
**5. Start server**
```sh
python manage.py migrate
python manage.py runserver
```

## Where to find Me
Me in [Telegram](https://t.me/yummy_lvl)
