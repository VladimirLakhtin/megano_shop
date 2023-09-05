from typing import Literal, Dict

from rest_framework.request import Request

from megano import settings
from products.models import Product


class Cart:
    def __init__(self, request: Request):
        self.session = request.session
        self.cart = self.session.setdefault(settings.CART_SESSION_ID, {})

    def save(self):
        self.session.save()

    def add(self, product_id: int, count: int) -> None:
        price = float(Product.objects.get(pk=product_id).price)
        product_info = self.cart.setdefault(str(product_id), {'count': 0})
        self.is_valid(method='POST', count=count,
                      product_info=product_info, product_id=product_id)
        product_info['count'] += count
        product_info['price'] = price
        self.save()

    def remove(self, product_id: int, count: int) -> None:
        product_id = str(product_id)
        product_info = self.cart.get(product_id)
        self.is_valid(method='DELETE',
                      count=count, product_info=product_info)
        if count == product_info.get('count'):
            del self.cart[product_id]
        else:
            product_info['count'] -= count
        self.save()

    @staticmethod
    def is_valid(method: Literal['DELETE', 'POST'], count: int,
                 product_info: Dict, product_id: int = None):
        if method == 'POST':
            product = Product.objects.get(pk=product_id)
            new_count = product_info['count'] + count
            if product.count < new_count:
                raise ValueError('The quantity of the product is not enough')

        if method == 'DELETE':
            if not product_info:
                raise ValueError('There is no such product in the cart')
            if product_info['count'] < count:
                raise ValueError('There is no such quantity of product in the basket')
