import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Creates an admin user non-interactively from environment variables."

    def handle(self, *args, **options):
        USERNAME = os.environ.get("ADMIN_USERNAME")
        EMAIL = os.environ.get("ADMIN_EMAIL")
        PASSWORD = os.environ.get("ADMIN_PASSWORD")

        if not all([USERNAME, EMAIL, PASSWORD]):
            self.stdout.write(
                self.style.WARNING(
                    "Admin credentials not found in environment variables. Skipping."
                )
            )
            return

        if User.objects.filter(username=USERNAME).exists():
            self.stdout.write(
                self.style.SUCCESS(f"Admin user '{USERNAME}' already exists. Skipping.")
            )
        else:
            self.stdout.write(self.style.SUCCESS(f"Creating admin user: {USERNAME}"))
            User.objects.create_superuser(
                username=USERNAME, email=EMAIL, password=PASSWORD
            )
