from django.core.management import BaseCommand

from accounts.models import Profile
from orders.models import Order, OrderDeliveryType, OrderPaymentType, OrderStatus
from products.models import Product


class Command(BaseCommand):
    """Create 5 orders"""

    def handle(self, *args, **options):
        self.stdout.write('Create orders')
        products = Product.objects.all()
        profiles = Profile.objects.all()
        deliveryTypes = [
            OrderDeliveryType.objects.get_or_create(title='free')[0],
            OrderDeliveryType.objects.get_or_create(title='paid')[0],
        ]
        paymentTypes = [
            OrderPaymentType.objects.get_or_create(title='paid')[0],
            OrderPaymentType.objects.get_or_create(title='awaiting payment')[0],
        ]
        counts = [1, 2, 5, 10, 20]
        statuses = OrderStatus.objects.all()
        cities = ['Moscow', 'Krasnodar', 'Donetsk', 'Saratov', 'Samara']
        addresses = ['Krasnaya st. 24 54', 'Selesnyova st. 12 23',
                     'Artyoma ave. 143 23', 'Bloka st. 214 21', 'Pushkina ave. 124 43']
        orders = [
            Order.objects.get_or_create(
                profile=profiles[i % 2],
                deliveryType=deliveryTypes[i % 2],
                paymentType=paymentTypes[i % 2],
                totalCost=products[i].price * counts[i],
                status=statuses[i],
                city=cities[i],
                address=addresses[i],
            )[0]
            for i in range(5)
        ]

        for i, product in enumerate(products[:5]):
            orders[i].products.add(product)

        orders_str = [str(orders) for orders in orders]
        self.stdout.write(self.style.SUCCESS(f"Orders ({', '.join(orders_str)}) was successfully created"))
