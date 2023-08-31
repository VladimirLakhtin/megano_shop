from rest_framework import serializers

from products.models import Product, ProductImage, Review, ProductSpecification, Sale


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for product review"""

    author = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = 'author', 'email', 'text', 'rate', 'date'

    def get_author(self, obj):
        return obj.author.fullName

    def get_email(self, obj):
        return obj.author.email

    def validate(self, attrs):
        """
        Method that verifies the uniqueness of review author under a product
        """

        profile = self.context.get('profile')
        product = self.context.get('product')
        if Review.objects.filter(author=profile,
                                 product=product).exists():
            msg = 'This user has already left a review for this product'
            raise serializers.ValidationError(msg)
        attrs['author'] = profile
        attrs['product'] = product
        return attrs


class ProductImageSerializer(serializers.ModelSerializer):
    """Serializer for product image"""

    class Meta:
        model = ProductImage
        fields = 'src', 'alt'


class ProductSpecificationSerializer(serializers.ModelSerializer):
    """Serializer for product specification"""

    class Meta:
        model = ProductSpecification
        fields = "id", "name", "value"


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for product"""

    images = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True)
    tags = serializers.SerializerMethodField()
    specifications = ProductSpecificationSerializer(many=True)

    class Meta:
        model = Product
        fields = ('id', 'category', 'price',
                  'count', 'date', 'title',
                  'description', 'fullDescription',
                  'freeDelivery', 'freeDelivery',
                  'rating', 'images', 'tags',
                  'reviews', 'specifications')

    def get_tags(self, obj):
        return list(obj.tags.values_list('name', flat=True))

    def get_images(self, instance):
        images = instance.images.all()
        if not images:
            default_image = ProductImage.get_default()
            return [ProductImageSerializer(default_image).data]

        images_data = [
            ProductImageSerializer(image).data
            for image in images
        ]
        return images_data


class SalesSerializer(serializers.ModelSerializer):
    """Serializer for product sale"""

    class Meta:
        model = Sale
        fields = 'id', 'price', 'salePrice', 'dateFrom', 'dateTo', 'title', 'images'
