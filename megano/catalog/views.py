from django.db.models import Avg, Count
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

    queryset = Category.objects\
        .filter(parent__isnull=True)\
        .all()\
        .select_related('image')\
        .prefetch_related('children__image')
    serializer_class = CategorySerializer


class TagsListView(ListAPIView):
    """View for list of products tags"""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = [CatalogTagsFilterBackend]


class BaseCatalogListView(ListAPIView):
    """Base view for a list products in catalog"""

    serializer_class = CatalogSerializer

    def get_queryset(self):
        return Product.objects.all() \
        .annotate(rating=Avg('reviews__rate'),
                  count_reviews=Count('reviews')) \
        .prefetch_related('tags') \
        .prefetch_related('images')


class CatalogListView(BaseCatalogListView):
    """View for a list of products in catalog"""

    pagination_class = CustomPagination
    filter_backends = [CatalogProductsOrderingFilter]

    def filter_queryset(self, queryset):
        return CatalogProductsOrderingFilter().filter_queryset(self.request, queryset, self)

class PopularProductsListView(BaseCatalogListView):
    """View for a list of popular products"""

    # filter_backends = [PopularProductsOrderingFilter]

    def filter_queryset(self, queryset):
        return queryset.order_by('sort_index')[:8]


class LimitedProductsListView(BaseCatalogListView):
    """View for a list of limited products"""

    def filter_queryset(self, queryset):
        return queryset[:16]


class BannersListView(BaseCatalogListView):
    """View for a list of banner products"""

    def filter_queryset(self, queryset):
        return queryset.order_by('?')[:5]


class SalesListView(ListAPIView):
    """View for a list of products sales"""

    queryset = Sale.objects.all()\
        .select_related('product')\
        .prefetch_related('product__images')
    serializer_class = SaleSerializer
    pagination_class = CustomPagination
