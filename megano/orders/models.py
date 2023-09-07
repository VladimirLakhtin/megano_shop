from django.db import models

from accounts.models import Profile
from products.models import Product


class Status(models.Model):
    title = models.CharField(max_length=50)

    @classmethod
    def get_default(cls):
        return cls.objects.get_or_create(title='placed')[0]


class DeliveryType(models.Model):
    title = models.CharField(max_length=30)


class PaymentType(models.Model):
    title = models.CharField(max_length=30)


class Order(models.Model):

    profile = models.ForeignKey(
        Profile,
        related_name='orders',
        on_delete=models.PROTECT
    )
    createdAt = models.DateTimeField(auto_now=True)
    deliveryType_id = models.ForeignKey(
        DeliveryType,
        related_name='orders',
        on_delete=models.PROTECT,
        null=True,
    )
    paymentType_id = models.ForeignKey(
        PaymentType,
        related_name='orders',
        on_delete=models.PROTECT,
        null=True
    )
    totalCost = models.DecimalField(
        default=0,
        max_digits=10,
        decimal_places=2,
    )
    status_id = models.ForeignKey(
        Status,
        related_name='orders',
        on_delete=models.PROTECT,
        default=Status.get_default(),
    )
    city = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    products = models.ManyToManyField(
        Product,
        related_name='orders',
        through='OrderProducts',
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
        return f'{self.__class__}(username={self.profile.fullName}, totalCost={self.totalCost})'

    class Meta:
        ordering = ('-createdAt',)


class OrderProducts(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    count = models.PositiveIntegerField()
