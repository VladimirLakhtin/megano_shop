from django.db import models

from accounts.models import Profile
from products.models import Product


class Status(models.Model):
    """Order status model"""

    title = models.CharField(max_length=50)

    @classmethod
    def get_default_pk(cls):
        return cls.objects.get_or_create(title="placed")[0].pk

    def __str__(self) -> str:
        return self.title


class DeliveryType(models.Model):
    """Delivery type order model"""

    title = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.title


class PaymentType(models.Model):
    """Payment type order model"""

    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title


class Order(models.Model):
    """Order model"""

    profile = models.ForeignKey(
        Profile, related_name="orders", on_delete=models.PROTECT
    )
    createdAt = models.DateTimeField(auto_now=True)
    deliveryType_id = models.ForeignKey(
        DeliveryType,
        related_name="orders",
        on_delete=models.PROTECT,
        null=True,
    )
    paymentType_id = models.ForeignKey(
        PaymentType, related_name="orders", on_delete=models.PROTECT, null=True
    )
    totalCost = models.DecimalField(
        default=0,
        max_digits=10,
        decimal_places=2,
    )
    status_id = models.ForeignKey(
        Status,
        related_name="orders",
        on_delete=models.PROTECT,
        default=Status.get_default_pk,
    )
    city = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    products = models.ManyToManyField(
        Product,
        related_name="orders",
        through="OrderProducts",
    )

    @property
    def status(self) -> Status:
        return self.status_id.title

    @property
    def deliveryType(self) -> DeliveryType:
        return self.deliveryType_id.title

    @property
    def paymentType(self) -> PaymentType:
        return self.paymentType_id.title

    def __str__(self) -> str:
        return f"{self.__class__}(username={self.profile.fullName}, totalCost={self.totalCost})"

    class Meta:
        ordering = ("-createdAt",)


class OrderProducts(models.Model):
    """Custom may-to-many through model for Product and Order"""

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    count = models.PositiveIntegerField()
