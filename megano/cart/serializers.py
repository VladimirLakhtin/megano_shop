from rest_framework import serializers

from catalog.serializers import CatalogSerializer


class CartSerializer(CatalogSerializer):
    """Serializer for get data of products in cart"""

    count = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    def get_count(self, obj):
        count = self.context.get(obj.pk)
        return count or self.context['cart'][str(obj.pk)]['count']

    def get_price(self, obj):
        return obj.salePrice or obj.price
