import random

from django.core.management import BaseCommand

from accounts.models import Profile
from products.models import Review, Product


class Command(BaseCommand):
    """Create 5 products"""

    def handle(self, *args, **options):
        self.stdout.write('Create tags')
        texts = ["I'm good customer. I like this product", "I'm bad customer. I hate this product"]
        users = list(Profile.objects.all())
        products = list(Product.objects.all())
        reviews = [
            str(
                Review.objects.get_or_create(
                    author=users[i % 2],
                    text=texts[i % 2],
                    rate=i % 5 + 1,
                    product=products[i % 5],
                )[0]
            )
            for i in range(10)
        ]
        self.stdout.write(self.style.SUCCESS(f"Reviews ({', '.join(reviews)}) was successfully created"))
