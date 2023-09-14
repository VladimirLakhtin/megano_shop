from typing import List, Dict

from django.db import models
from django.db.models import Count, QuerySet
from rest_framework import serializers

from catalog.models import Category, CategoryImage
from products.models import Product, Sale
from products.serializers import ProductSerializer, TagSerializer


class CategoryImageSerializer(serializers.ModelSerializer):
    """Serializer for product category image"""

    class Meta:
        model = CategoryImage
        fields = "src", "alt"


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for product category"""

    image = CategoryImageSerializer()
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = "id", "title", "image", "subcategories"

    def get_subcategories(self, obj: Category) -> List[Dict]:
        subcategories = list(obj.children.all())
        subcategories_data = [
            {
                "id": subcategory.pk,
                "title": subcategory.title,
                "image": CategoryImageSerializer(subcategory.image).data,
            }
            for subcategory in subcategories
        ]
        return subcategories_data


class CatalogSerializer(ProductSerializer):
    """Serializer for product item in catalog"""

    reviews = serializers.IntegerField(source='count_reviews')
    tags = TagSerializer(many=True)

    class Meta:
        model = Product
        fields_to_remove = {"fullDescription", "specifications"}
        parent_fields = set(ProductSerializer.Meta.fields)
        fields = tuple(parent_fields - fields_to_remove)


class SaleSerializer(serializers.ModelSerializer):
    """Serializer for instance of Sale"""

    id = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = Sale
        fields = "id", "price", "salePrice", "dateFrom", "dateTo", "title", "images"

    def get_id(self, obj: Sale) -> int:
        return obj.product.id

    def get_price(self, obj: Sale) -> float:
        return obj.product.price

    def get_title(self, obj: Sale) -> str:
        return obj.product.title

    def get_images(self, obj: Sale) -> List[str]:
        return [str(img.src) for img in obj.product.get_images]
