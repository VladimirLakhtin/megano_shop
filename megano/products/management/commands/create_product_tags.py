from django.core.management import BaseCommand

from products.models import Tag


class Command(BaseCommand):
    """Create 11 tags"""

    def handle(self, *args, **options):
        self.stdout.write("Create tags")
        names = [
            "Apple",
            "Windows",
            "China",
            "Xiaomi",
            "AMD",
            "Intel",
            "MacOS",
            "M1",
            "M2",
            "Wireless charge",
            "Noise reduction",
        ]
        tags = [str(Tag.objects.get_or_create(name=name)[0]) for name in names]
        self.stdout.write(
            self.style.SUCCESS(f"Tags ({', '.join(tags)}) was successfully created")
        )
