from django.core.management import BaseCommand

from catalog.models import Category


class Command(BaseCommand):
    """Create 3 categories and 6 subcategories"""

    def handle(self, *args, **options):
        self.stdout.write('Create categories')
        category_structure = {
            'PC': ['Laptop', 'Desktop'],
            'Smartphone': ['Android', 'Iphone'],
            'Accessories': ['Headphones', 'Mouses'],
        }
        for category, subcategories in category_structure.items():
            category, _ = Category.objects.get_or_create(name=category)
            category_subcategories = list(category.children.all())
            for subcategory in subcategories:
                if subcategory not in category_subcategories:
                    subcategory, _ = Category.objects.get_or_create(name=subcategory)
                    category.children.add(subcategory)

        self.stdout.write(self.style.SUCCESS(f"Categories ({category_structure}) was successfully created"))
