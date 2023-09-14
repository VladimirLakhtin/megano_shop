from django.db.models import Count, Avg, Max
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.cart import Cart
from cart.serializers import CartSerializer
from products.models import Product


class CartApiView(APIView):
    """View for get cart info, add and delete items"""

    def get(self, request: Request) -> Response:
        cart = Cart(request)
        queryset = Product.objects.all() \
            .filter(pk__in=cart.cart.keys()) \
            .annotate(rating=Avg('reviews__rate'),
                      count_reviews=Count('reviews'),
                      max_sale=Max('sales__sale')) \
            .prefetch_related('tags') \
            .prefetch_related('images')
        serializer = CartSerializer(queryset, many=True, context={"cart": cart.cart})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        cart = Cart(request)
        try:
            cart.add(
                product_id=request.data.get("id"),
                count=int(request.data.get("count")),
            )
            print('')
        except ValueError as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        data = self.get(request).data
        return Response(data, status=status.HTTP_200_OK)

    def delete(self, request: Request) -> Response:
        cart = Cart(request)
        try:
            cart.remove(
                product_id=request.data.get("id"),
                count=request.data.get("count"),
            )
        except ValueError as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        data = self.get(request).data
        return Response(data, status=status.HTTP_200_OK)
