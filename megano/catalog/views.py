from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from catalog.models import Category
from catalog.serializers import CategorySerializer, CatalogSerializer
from products.models import Product, Tag
from catalog.serializers import TagSerializer


class CategoriesListView(ListAPIView):
    """View for a list of products categories"""

    queryset = Category.objects.filter(parent__isnull=True).all()
    serializer_class = CategorySerializer


class TagsListView(ListAPIView):
    """View for list of products tags"""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class CatalogListView(APIView):
    def get(self, request: Request) -> Response:
        params = request.GET
        query = {
            ''
        }
        products = Product.objects.filter(query)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class PopularProductsListView(ListAPIView):
    """View for a list of popular products"""

    ...


class LimitedProductsListView(ListAPIView):
    """View for a list of limited products"""

    queryset = Product.objects.filter(is_limited=True)
    serializer_class = CatalogSerializer


class SalesListView(ListAPIView):
    """View for a list of products sales"""

    ...



class BannersListView(ListAPIView):
    """View for a list of banner products"""

    ...
