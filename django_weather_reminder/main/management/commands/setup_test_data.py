from django.db import transaction
from django.core.management.base import BaseCommand
from .functions_for_fake_data_create import *

NUM_USERS = 200
NUM_CITIES = 100
PERIODS_LIST = [1, 2, 3, 6, 12, 24]
NUM_SUBSCRIBERS = 200


class Command(BaseCommand):
    help = "Generates test data"

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Deleting old data...")

        delete_all_data()
        people = create_fake_users(NUM_USERS)
        cities = create_fake_cities(NUM_CITIES)
        periods = create_fake_periods(PERIODS_LIST)

        create_fake_subscribers(NUM_SUBSCRIBERS, people, cities, periods)
