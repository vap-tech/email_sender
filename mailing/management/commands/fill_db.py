from django.core.management import BaseCommand


import os


class Command(BaseCommand):

    def handle(self, *args, **options):

        os.system('python3 manage.py loaddata data.json')
