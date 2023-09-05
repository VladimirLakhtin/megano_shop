from django.shortcuts import render
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.models import Order
from orders.serializers import OrderSerializer


class OrdersAPIView(APIView):

    def get(self, request: Request) -> Response:
        profile = request.user.profile
        queryset = Order.objects.filter(profile=profile)
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data,
            status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
