from django.db.models import Count
from rest_framework import serializers

from catalog.models import Category, CategoryImage
from products.models import Product, Tag
from products.serializers import ProductSerializer


class CategoryImageSerializer(serializers.ModelSerializer):
    """Serializer for product category image"""

    class Meta:
        model = CategoryImage
        fields = 'src', 'alt'


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for product category"""

    image = CategoryImageSerializer()
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = 'id', 'title', 'image', 'subcategories'

    def get_subcategories(self, obj):
        subcategories = list(obj.children.all())
        subcategories_data = [
            {
                'id': subcategory.pk,
                'title': subcategory.title,
                'image': CategoryImageSerializer(subcategory.image).data,
            }
            for subcategory in subcategories
        ]
        return subcategories_data


class TagSerializer(serializers.ModelSerializer):
    """Serializer for product tag"""

    class Meta:
        model = Tag
        fields = 'id', 'name'


class CatalogSerializer(ProductSerializer):
    """Serializer for product item in catalog"""

    reviews = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)

    class Meta:
        model = Product
        fields_to_remove = {'fullDescription', 'specifications'}
        parent_fields = set(ProductSerializer.Meta.fields)
        fields = tuple(parent_fields - fields_to_remove)

    def get_reviews(self, obj):
        return obj.reviews.aggregate(Count("text")).get('text__count')
