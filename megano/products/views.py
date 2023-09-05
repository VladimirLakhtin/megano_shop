from rest_framework.generics import RetrieveAPIView, CreateAPIView

from products.models import Product
from products.serializers import ProductSerializer, ReviewSerializer

from products.models import Review


class ProductDetailView(RetrieveAPIView):
    """View for product details"""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CreateReviewView(CreateAPIView):
    """View for creating product review"""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_serializer_context(self):
        result = super().get_serializer_context()
        result['product_pk'] = self.kwargs['pk']
        return result
