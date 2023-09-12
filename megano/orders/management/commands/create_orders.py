from django.core.management import BaseCommand

from accounts.models import Profile
from orders.models import Order, DeliveryType, PaymentType, Status, OrderProducts
from products.models import Product


class Command(BaseCommand):
    """Create 5 orders"""

    def handle(self, *args, **options):
        self.stdout.write("Create orders")
        products = Product.objects.all()
        profiles = Profile.objects.all()
        deliveryTypes = [
            DeliveryType.objects.get_or_create(title="ordinary")[0],
            DeliveryType.objects.get_or_create(title="express")[0],
        ]
        paymentTypes = [
            PaymentType.objects.get_or_create(title="online")[0],
            PaymentType.objects.get_or_create(title="someone")[0],
        ]
        counts = [1, 2, 5, 10, 20]
        statuses = Status.objects.all()
        cities = ["Moscow", "Krasnodar", "Donetsk", "Saratov", "Samara"]
        addresses = [
            "Krasnaya st. 24 54",
            "Selesnyova st. 12 23",
            "Artyoma ave. 143 23",
            "Bloka st. 214 21",
            "Pushkina ave. 124 43",
        ]
        orders = [
            Order.objects.get_or_create(
                profile=profiles[i % 2],
                deliveryType_id=deliveryTypes[i % 2],
                paymentType_id=paymentTypes[i % 2],
                totalCost=products[i].price * counts[i],
                status_id=statuses[i],
                city=cities[i],
                address=addresses[i],
            )[0]
            for i in range(5)
        ]

        for i, product in enumerate(products[:5]):
            OrderProducts.objects.get_or_create(
                order=orders[i], product=product, count=counts[i]
            )

        orders_str = [str(orders) for orders in orders]
        self.stdout.write(
            self.style.SUCCESS(
                f"Orders ({', '.join(orders_str)}) was successfully created"
            )
        )
