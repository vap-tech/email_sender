from django.core.mail import send_mail
from django.core.management import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        result = send_mail(
            'Покупка',
            'Привет, решили не покупать.',
            'admin@v-petrenko.ru',
            ['bafomet2016vitt@gmail.com'],
            fail_silently=False,
        )
        print(result)
