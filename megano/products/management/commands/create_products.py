import random

from django.core.management import BaseCommand

from catalog.models import Category
from products.models import Tag, Product


class Command(BaseCommand):
    """Create 5 products"""

    def handle(self, *args, **options):
        self.stdout.write('Create products')
        product_titles = ['Apple Mac Pro', 'Xiaomi bluetooth headphones',
                          'Iphone 14 pro', 'Lenovo a156', 'Magic Mouse']
        categories_names = ['Desktop', 'Headphones', 'Iphone', 'Laptop', 'Mouses']
        tags = list(Tag.objects.all())
        prices = list(range(100, 1001, 200))
        counts = list(range(10, 101, 20))
        products = [
            Product.objects.get_or_create(
                title=product_titles[i],
                price=prices[i],
                count=counts[i],
                description=f"Cool {product_titles[i]}",
                fullDescription=f"Realy cool {product_titles[i]}",
                category=Category.objects.get(name=categories_names[i]),
                is_limited=bool(i % 2),
                freeDelivery=bool(i % 3),
            )
            for i in range(5)
        ]

        for product in products[:5]:
            if product[1]:
                tag_1 = random.choice(tags)
                tag_2 = random.choice(tags)
                product[0].tags.add(tag_1)
                if tag_1 != tag_2:
                    product[0].tags.add(tag_2)

        products_str = [str(product[0]) for product in products]
        self.stdout.write(self.style.SUCCESS(f"Products ({', '.join(products_str)}) was successfully created"))
