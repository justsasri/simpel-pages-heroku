from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()

class Command(BaseCommand):
    help = "Init Demo User"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        try:
            botmin = User.objects.get(username="demo_admin")
        except User.DoesNotExist:
            botmin = User.objects.create_user(
                username="demo_admin",
                password="demo_pass",
                email="demo.admin@email.com",
                first_name="Admin",
                is_staff=True,
                is_superuser=True,
            )
        botmin.save()
        print("demo_admin has been created with password: demo_pass")
