from rest_framework import status
from rest_framework.generics import get_object_or_404, RetrieveAPIView, CreateAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import Product, Tag
from products.serializers import ProductSerializer, ReviewSerializer


class ProductDetailView(RetrieveAPIView):
    """View for product details"""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CreateReviewView(CreateAPIView):
    """View for creating product review"""

    queryset = 

    def post(self, request: Request, pk) -> Response:
        product = get_object_or_404(Product, pk=pk)
        profile = request.user.profile

        serializer = ReviewSerializer(
            data=request.data,
            context={'product': product, 'profile': profile}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
