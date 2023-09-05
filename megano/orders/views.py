from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.cart import Cart
from orders.models import Order
from orders.serializers import OrderSerializer, CreateOrderSerializer


class OrdersAPIView(APIView):

    def get(self, request: Request) -> Response:
        profile = request.user.profile
        queryset = Order.objects.filter(profile=profile)
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        cart = Cart(request)
        products_data = request.data
        orders_data = {
            'profile': request.user.profile.pk,
            'products': [p.get('id') for p in products_data],
        }
        serializer = CreateOrderSerializer(data=orders_data, context={'cart': cart})

        if serializer.is_valid():
            order = serializer.save()
            return Response(data={'orderId': order.pk},
                            status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
