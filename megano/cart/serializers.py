from rest_framework import serializers

from catalog.serializers import CatalogSerializer
from products.models import Product


class CartSerializer(CatalogSerializer):
    """Serializer for get data of products in cart"""

    count = serializers.SerializerMethodField()

    def get_count(self, obj):
        return self.context['cart'][str(obj.pk)]['count']
