import os

from django.core.management import BaseCommand

from users.models import User, Country


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email=os.getenv('SU_MAIL'),
            first_name='Fox',
            last_name='Kot',
            country=Country.objects.first(),
            is_staff=True,
            is_superuser=True,
        )
        user.set_password(os.getenv('SU_PASS'))
        user.save()
