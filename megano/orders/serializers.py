from rest_framework import serializers

from cart.serializers import CartSerializer
from catalog.serializers import CatalogSerializer
from orders.models import Order, PaymentType, OrderProducts, DeliveryType
from products.models import Product


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for get order info"""

    fullName = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    products = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            "id",
            "createdAt",
            "deliveryType",
            "paymentType",
            "totalCost",
            "status",
            "city",
            "address",
            "fullName",
            "phone",
            "email",
            "products",
        )

    def get_fullName(self, obj: Order):
        return obj.profile.fullName

    def get_phone(self, obj: Order):
        return obj.profile.phone

    def get_email(self, obj: Order):
        return obj.profile.email

    def get_products(self, obj: Order):
        product_counts = {
            relation.product.pk: relation.count
            for relation in obj.orderproducts_set.all()
        }
        queryset = obj.products.all()\
            .annotate(rating=Avg('reviews__rate'),
                      count_reviews=Count('reviews'))\
            .prefetch_related('tags')\
            .prefetch_related('images')
        serializer = CartSerializer(
            obj.products.all(), many=True, context=product_counts
        )
        return serializer.data


class CreateOrderSerializer(serializers.ModelSerializer):
    """Serializer for create order"""

    class Meta:
        model = Order
        fields = ("profile",)

    def create(self, validated_data):
        cart = self.context.get("cart")
        order = Order.objects.create(
            profile=validated_data.get("profile"),
            totalCost=cart.get_total_cost(),
        )

        for product_id in cart.cart.keys():
            OrderProducts.objects.get_or_create(
                order=order,
                product=Product.objects.get(pk=product_id),
                count=cart.cart[product_id]["count"],
            )
        return order


class UpdateOrderSerializer(serializers.ModelSerializer):
    """Serializer for update order info"""

    deliveryType = serializers.CharField(required=False)
    paymentType = serializers.CharField(required=False)

    class Meta:
        model = Order
        fields = "city", "address", "deliveryType", "paymentType", "totalCost"

    def validate(self, attrs):
        # check existing delivery type
        delivery_types = DeliveryType.objects.values_list("title", flat=True)
        deliveryType = attrs.get("deliveryType")
        if attrs.get("deliveryType") not in delivery_types:
            raise ValueError(f'Delivery type "{deliveryType}" is not exists')

        # check existing payment type
        payment_types = PaymentType.objects.values_list("title", flat=True)
        paymentType = attrs.get("paymentType")
        if attrs.get("paymentType") not in payment_types:
            raise ValueError(f'Payment type "{paymentType}" is not exists')

        # add delivery and payment type ids in attrs
        attrs["deliveryType_id"] = DeliveryType.objects.get(title=deliveryType).pk
        attrs["paymentType_id"] = PaymentType.objects.get(title=paymentType).pk
        del attrs["deliveryType"]
        del attrs["paymentType"]

        # increase in total cost depending on delivery
        if deliveryType == "express":
            attrs["totalCost"] += 50
        elif attrs["totalCost"] < 200:
            attrs["totalCost"] += 20

        return attrs

    def update(self, instance, validated_data):
        Order.objects.filter(pk=instance.pk).update(**validated_data)
        for product in instance.products.all():
            relationship = product.orderproducts_set.get(order=instance.pk)
            product.count -= relationship.count
            product.save()

        return instance
