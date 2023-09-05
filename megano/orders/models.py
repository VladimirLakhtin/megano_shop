from django.db import models

from accounts.models import Profile
from products.models import Product


class OrderStatus(models.Model):
    title = models.CharField(max_length=50)


class OrderDeliveryType(models.Model):
    title = models.CharField(max_length=30)


class OrderPaymentType(models.Model):
    title = models.CharField(max_length=30)


class Order(models.Model):

    profile = models.ForeignKey(
        Profile,
        related_name='orders',
        on_delete=models.PROTECT
    )
    createdAt = models.DateTimeField(auto_now=True)
    deliveryType_id = models.ForeignKey(
        OrderDeliveryType,
        related_name='orders',
        on_delete=models.PROTECT,
    )
    paymentType_id = models.ForeignKey(
        OrderPaymentType,
        related_name='orders',
        on_delete=models.PROTECT,
    )
    totalCost = models.DecimalField(
        default=0,
        max_digits=10,
        decimal_places=2,
    )
    status_id = models.ForeignKey(
        OrderStatus,
        related_name='orders',
        on_delete=models.PROTECT,
    )
    city = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    products = models.ManyToManyField(Product, related_name='orders')

    @property
    def status(self) -> OrderStatus:
        return self.status_id.title

    @property
    def deliveryType(self) -> OrderDeliveryType:
        return self.deliveryType_id.title

    @property
    def paymentType(self) -> OrderPaymentType:
        return self.paymentType_id.title

    def __str__(self) -> str:
        return f'{self.__class__}(username={self.profile.fullName}, totalCost={self.totalCost})'

    class Meta:
        ordering = ('-createdAt',)
