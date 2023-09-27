from django.core.management import BaseCommand

import mailing.services


class Command(BaseCommand):

    def handle(self, *args, **options):

        mailing.services.send_all()
