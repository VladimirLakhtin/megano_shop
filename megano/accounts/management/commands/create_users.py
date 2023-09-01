from django.contrib.auth.models import User
from django.core.management import BaseCommand

from accounts.models import Profile


class Command(BaseCommand):
    """Create 2 users"""

    def handle(self, *args, **options):
        self.stdout.write('Create users')
        user_1 = User.objects.create_user(username='vllakhtin', password='vllakhtin')
        Profile.objects.create(user=user_1, fullName='Vladimir')
        user_2 = User.objects.create_user(username='alina', password='alina')
        Profile.objects.create(user=user_2, fullName='Alina')
        self.stdout.write(self.style.SUCCESS(f"Users {(user_1, user_2)} was successfully created"))
