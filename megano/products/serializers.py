from typing import List

from django.db.models import Avg
from rest_framework import serializers

from products.models import (
    Product,
    ProductImage,
    Review,
    ProductSpecification,
    Sale,
    Tag,
)


class TagSerializer(serializers.ModelSerializer):
    """Serializer for product tag"""

    class Meta:
        model = Tag
        fields = "id", "name"


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for product review"""

    author = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = "author", "email", "text", "rate", "date"

    def get_author(self, obj: Product) -> str:
        return obj.author.fullName

    def get_email(self, obj: Product) -> str:
        return obj.author.email

    def validate(self, attrs):
        """
        Method that verifies the uniqueness of review author under a product
        """

        profile = self.context.get("request").user.profile
        product = Product.objects.get(pk=self.context.get("product_pk"))
        if Review.objects.filter(author=profile, product=product).exists():
            msg = "This user has already left a review for this product"
            raise serializers.ValidationError(msg)
        attrs["author"] = profile
        attrs["product"] = product
        return attrs


class ProductImageSerializer(serializers.ModelSerializer):
    """Serializer for product image"""

    class Meta:
        model = ProductImage
        fields = "src", "alt"


class ProductSpecificationSerializer(serializers.ModelSerializer):
    """Serializer for product specification"""

    class Meta:
        model = ProductSpecification
        fields = "id", "name", "value"


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for product"""

    images = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True)
    tags = TagSerializer(many=True)
    specifications = ProductSpecificationSerializer(many=True)
    rating = serializers.DecimalField(max_digits=2, decimal_places=1)

    class Meta:
        model = Product
        fields = (
            "id",
            "category",
            "price",
            "count",
            "date",
            "title",
            "description",
            "fullDescription",
            "freeDelivery",
            "freeDelivery",
            "rating",
            "images",
            "tags",
            "reviews",
            "specifications",
        )

    def get_images(self, obj: Product) -> List:
        images = obj.images.all()
        if not images:
            default_image = ProductImage.get_default()
            return [ProductImageSerializer(default_image).data]

        images_data = [ProductImageSerializer(image).data for image in images]
        return images_data



class SalesSerializer(serializers.ModelSerializer):
    """Serializer for product sale"""

    class Meta:
        model = Sale
        fields = "id", "price", "salePrice", "dateFrom", "dateTo", "title", "images"
