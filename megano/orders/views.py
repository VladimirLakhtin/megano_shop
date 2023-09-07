from datetime import datetime

from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.cart import Cart
from orders.models import Order, Status
from orders.serializers import OrderSerializer, CreateOrderSerializer, UpdateOrderSerializer


class OrdersAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        profile = request.user.profile
        queryset = Order.objects.filter(profile=profile)
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        cart = Cart(request)
        serializer = CreateOrderSerializer(
            data={'profile': request.user.profile.pk},
            context={'cart': cart}
        )
        if serializer.is_valid():
            order = serializer.save()
            return Response(data={'orderId': order.pk},
                            status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class OrderDetailsAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request: Request, id: int) -> Response:
        order = get_object_or_404(Order, pk=id)
        serializer = OrderSerializer(order)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)

    def post(self, request: Request, id: int) -> Response:
        order = Order.objects.get(pk=id)
        serializer = UpdateOrderSerializer(instance=order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'orderId': id},
                            status=status.HTTP_200_OK)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PaymentAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request: Request, id: int) -> Response:
        order = Order.objects.get(pk=id)
        if self.is_valid(**request.data):
            order.status_id = Status.objects.get(title='paid')
            order.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def is_valid(self, **kwargs):
        year = 2000 + int(kwargs['year'])
        month = int(kwargs['month'])
        validity_period = datetime(year=year, month=month, day=1)
        return datetime.now() >= validity_period \
            and len(kwargs['code']) == 3
