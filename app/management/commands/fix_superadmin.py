from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Fix superadmin account to have is_superuser=True'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username of the superadmin account')

    def handle(self, *args, **options):
        username = options['username']
        try:
            user = User.objects.get(username=username)
            user.is_superuser = True
            user.is_staff = True
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f'Successfully fixed {username}: is_superuser=True, is_staff=True')
            )
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'User {username} not found')
            )

