from rest_framework import serializers

from catalog.serializers import CatalogSerializer
from orders.models import Order, PaymentType, Status


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
        read_only_fields = 'createdAt',

    def get_fullName(self, obj: Order):
        return obj.profile.fullName

    def get_phone(self, obj: Order):
        return obj.profile.phone

    def get_email(self, obj: Order):
        return obj.profile.email


class CreateOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = 'profile', 'totalCost', 'products'

    def create(self, validated_data):
        order, _ = Order.objects.get_or_create(
            profile=validated_data.get('profile'),
            status_id=Status.get_default(),
            paymentType_id=PaymentType.get_default(),
            totalCost=self.context.get('cart').get_total_cost(),
        )
        for product in validated_data.get('products'):
            order.products.add(product)
        order.save()
        return order
