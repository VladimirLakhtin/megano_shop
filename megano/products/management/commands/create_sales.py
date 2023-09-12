import random

from django.core.management import BaseCommand

from products.models import Product, Sale


class Command(BaseCommand):
    """Create sales"""

    def handle(self, *args, **options):
        products = list(Product.objects.all())
        sales = [
            str(
                Sale.objects.get_or_create(
                    product=product,
                    sale=round(random.random(), 2) * 100,
                    dateFrom="2023-08-24",
                    dateTo="2023-12-31",
                )
            )
            for product in products
            if product.freeDelivery and product.count > 10
        ]
        self.stdout.write(
            self.style.SUCCESS(f"Sales ({', '.join(sales)}) was successfully created")
        )
