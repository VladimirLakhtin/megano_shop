from typing import Iterable, Optional

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Avg, Count

from accounts.models import Profile
from catalog.models import Category


class Tag(models.Model):
    """Product tag model"""

    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    """Product info model"""

    price = models.DecimalField(max_digits=6, decimal_places=2)
    count = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=256, null=False, blank=True)
    fullDescription = models.TextField(blank=True, null=False)
    freeDelivery = models.BooleanField(default=False)
    sort_index = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="products",
        null=True,
    )
    tags = models.ManyToManyField(
        Tag,
        related_name="products",
        blank=True,
    )
    is_limited = models.BooleanField(default=False)

    @property
    def salePrice(self) -> Optional[float]:
        sales = self.sales.values_list("sale", flat=True)
        if sales:
            return float(self.price) * (1 - float(max(sales)) / 100)

    # @property
    # def rating(self) -> float:
    #     """Get average rating for product"""
    #
    #     return float(self.reviews.aggregate(Avg("rate"))["rate__avg"])

    @property
    def get_images(self) -> Iterable:
        """Get product images or a default image"""

        images = self.images.all()
        if not images:
            return [ProductImage.get_default()]
        return images

    def __str__(self) -> str:
        return self.title


class ProductSpecification(models.Model):
    """Product specification model"""

    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="specifications"
    )
    name = models.CharField(max_length=256, default="")
    value = models.CharField(max_length=256, default="")

    class Meta:
        verbose_name = "Product specification"
        verbose_name_plural = "Product specifications"

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(product={self.product.title}, "
            f"name={self.name})"
        )


def get_product_image_path(instance: "ProductImage", filename: str) -> str:
    return f"products/images/product_{instance.product.pk}/{filename}"


class ProductImage(models.Model):
    """Product image model"""

    default_path = "products/images/default.png"

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
        null=True,
    )
    src = models.ImageField(
        upload_to=get_product_image_path,
        verbose_name="Ссылка",
    )

    @property
    def alt(self) -> str:
        if self.src == self.default_path:
            return "Default product image"
        return f"{self.product.title} image: {self.src.url.split('/')[-1]}"

    @classmethod
    def get_default(cls):
        image, _ = cls.objects.get_or_create(src=cls.default_path)
        return image

    def __str__(self) -> str:
        return self.alt


class Review(models.Model):
    """Product review info model"""

    author = models.ForeignKey(Profile, on_delete=models.PROTECT)
    text = models.TextField(blank=False, null=False)
    rate = models.PositiveIntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
    )
    date = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(product={self.product}, "
            f"author={self.author})"
        )


class Sale(models.Model):
    """Product sale model"""

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="sales",
    )
    sale = models.PositiveIntegerField(
        default=0,
    )
    dateFrom = models.DateField(default="")
    dateTo = models.DateField(blank=True, null=True)

    @property
    def salePrice(self) -> float:
        return round(float(self.product.price) * (1 - self.sale / 100), 0)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}" f"(product={self.product.title})"
