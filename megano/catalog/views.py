from rest_framework.generics import ListAPIView

from catalog.filters import (
    CatalogProductsOrderingFilter,
    CatalogTagsFilterBackend,
    PopularProductsOrderingFilter,
)
from catalog.models import Category
from catalog.pagination import CustomPagination
from catalog.serializers import CategorySerializer, CatalogSerializer, SaleSerializer
from products.models import Product, Tag, Sale
from catalog.serializers import TagSerializer


class CategoriesListView(ListAPIView):
    """View for a list of products categories"""

    queryset = Category.objects.filter(parent__isnull=True).all()
    serializer_class = CategorySerializer


class TagsListView(ListAPIView):
    """View for list of products tags"""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = [CatalogTagsFilterBackend]


class CatalogListView(ListAPIView):
    """View for a list of products in catalog"""

    queryset = Product.objects.all()
    serializer_class = CatalogSerializer
    pagination_class = CustomPagination
    filter_backends = [CatalogProductsOrderingFilter]


class PopularProductsListView(ListAPIView):
    """View for a list of popular products"""

    queryset = Product.objects.all()
    serializer_class = CatalogSerializer
    filter_backends = [PopularProductsOrderingFilter]


class LimitedProductsListView(ListAPIView):
    """View for a list of limited products"""

    queryset = Product.objects.filter(is_limited=True)[:16]
    serializer_class = CatalogSerializer


class SalesListView(ListAPIView):
    """View for a list of products sales"""

    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    pagination_class = CustomPagination


class BannersListView(ListAPIView):
    """View for a list of banner products"""

    queryset = Product.objects.order_by("?")[:5]
    serializer_class = CatalogSerializer
