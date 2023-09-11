import random

from django.core.management import BaseCommand

from accounts.models import Profile
from products.models import Review, Product


class Command(BaseCommand):
    """Create reviews"""

    def handle(self, *args, **options):
        self.stdout.write('Create reviews')
        texts = ["I'm good customer. I like this product", "I'm bad customer. I hate this product", "I don't care"]
        users = list(Profile.objects.all())
        products = list(Product.objects.all())
        reviews = [
            str(
                Review.objects.get_or_create(
                    author=users[i % 2],
                    text=texts[i % 2],
                    rate=random.randint(1, 5),
                    product=products[i // 2],
                )[0]
            )
            for i in range(len(products)*2)
            if i % 5 != 0
        ]

        self.stdout.write(self.style.SUCCESS(f"Reviews ({', '.join(reviews)}) was successfully created"))
