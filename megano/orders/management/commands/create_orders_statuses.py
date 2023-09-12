from django.core.management import BaseCommand

from orders.models import Status


class Command(BaseCommand):
    """Create 5 statuses"""

    def handle(self, *args, **options):
        self.stdout.write("Create statuses")
        titles = ["placed", "awaiting payment", "paid", "confirmed", "canceled"]
        statuses = [
            str(Status.objects.get_or_create(title=title)[0]) for title in titles
        ]
        self.stdout.write(
            self.style.SUCCESS(
                f"Statuses ({', '.join(statuses)}) was successfully created"
            )
        )
