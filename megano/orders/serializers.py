from rest_framework import serializers

from catalog.serializers import CatalogSerializer
from orders.models import Order


class OrderSerializer(serializers.ModelSerializer):
    fullName = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    products = CatalogSerializer(many=True)

    class Meta:
        model = Order
        fields = 'createdAt', 'deliveryType', 'paymentType', 'totalCost', \
                 'status', 'city', 'address', 'fullName', 'phone', 'email', \
                 'products'

    def get_fullName(self, obj: Order):
        return obj.profile.fullName

    def get_phone(self, obj: Order):
        return obj.profile.phone

    def get_email(self, obj: Order):
        return obj.profile.email