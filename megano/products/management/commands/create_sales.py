import random

from django.core.management import BaseCommand

from products.models import Product, Sale


class Command(BaseCommand):
    """Create 5 products"""

    def handle(self, *args, **options):
        products = list(Product.objects.all())
        sales = [
            str(
                Sale.objects.get_or_create(
                    product=products[i],
                    salePrice=float(products[i].price) * 0.8,
                    dateFrom='2023-08-24',
                    dateTo='2023-12-31',
                )
            )
            for i in range(5)
        ]
        self.stdout.write(self.style.SUCCESS(f"Sales ({', '.join(sales)}) was successfully created"))
