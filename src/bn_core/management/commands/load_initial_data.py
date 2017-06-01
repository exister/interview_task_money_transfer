from django.core.management import BaseCommand

from bn_users.initial_data import load_data as load_users_data


class Command(BaseCommand):
    def handle(self, *args, **options):
        load_users_data()
