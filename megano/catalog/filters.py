from django.db.models import Q
from rest_framework import filters

from catalog.models import Category
from products.models import Product


class CatalogProductsOrderingFilter(filters.OrderingFilter):

    def get_ordering(self, request, queryset, view):
        sort_param = request.GET.get('sort')
        sort_type = request.GET.get('sortType')
        sort_symbol = '-' if sort_type == 'dec' else ''
        if sort_param == 'rating':
            return sorted(
                queryset,
                key=lambda x: x.rating,
                reverse=sort_type == 'dec'
            )
        return queryset.order_by(sort_symbol + sort_param)

    def filter_queryset(self, request, queryset, view):
        data = request.GET
        category = Category.objects.filter(pk=data.get('category')).first()
        category_children = category.children.all() if category else None
        params = {
            'category': None if category_children else category,
            'category__in': category_children if category_children else None,
            'title__contains': data.get('filter[name]'),
            'price__gte': int(data.get('filter[minPrice]')),
            'price__lte': int(data.get('filter[maxPrice]')),
            'freeDelivery': True if data.get('filter[freeDelivery]') == 'true' else None,
            'count__gte': 1 if data.get('filter[available]') == 'true' else None,
            'tags__in': data.get('tags[]'),
        }
        actual_params = {k: v for k, v in params.items() if v is not None}
        queryset = queryset.filter(**actual_params)
        queryset = self.get_ordering(request, queryset, view)
        return queryset


class CatalogTagsFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        category_pk = request.GET.get('category')
        if category_pk:
            category = Category.objects.get(pk=category_pk)
            children_categories = list(category.children.all())
            categories = [category] + children_categories
            products = Product.objects.filter(
                Q(category__in=categories) | Q(category__children__in=categories)
            )
            queryset = queryset.filter(products__in=products).distinct()
        return queryset


class PopularProductsOrderingFilter(filters.OrderingFilter):
    def get_ordering(self, request, queryset, view):
        queryset.order_by('sort_index')
        return queryset

    def filter_queryset(self, request, queryset, view):
        return queryset[:8]
