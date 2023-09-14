from rest_framework import serializers

from catalog.serializers import CatalogSerializer
from products.models import Product


class CartSerializer(CatalogSerializer):
    """Serializer for get data of products in cart"""

    count = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    def get_count(self, obj: Product):
        count = self.context.get(obj.pk)
        return count or self.context["cart"][str(obj.pk)]["count"]

    def get_price(self, obj: Product):
        try:
            return float(obj.price) * (1 - float(obj.max_sale) / 100)
        except AttributeError:
            return obj.price
