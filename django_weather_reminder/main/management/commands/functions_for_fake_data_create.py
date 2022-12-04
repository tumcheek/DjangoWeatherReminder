import random

from .factories import *
from ...models import *
from faker import Faker


def delete_all_data():
    UserModel.objects.all().delete()
    CityModel.objects.all().delete()
    PeriodModel.objects.all().delete()
    SubscribersModel.objects.all().delete()


def create_fake_users(num_users):
    people = []
    for _ in range(num_users):
        person = UserFactory()
        people.append(person)
    return people


def create_fake_cities(num_cities):
    cities = []
    for _ in range(num_cities):
        city = CityFactory()
        cities.append(city)
    return cities


def create_fake_periods(periods_list):
    periods = []
    for _period in periods_list:
        period = PeriodFactory(period_of_notice=_period)
        periods.append(period)
    return periods


def create_fake_subscribers(num_subscribers, people, cities, periods):
    for _ in range(num_subscribers):
        SubscribersFactory(user=random.choice(people), city=random.choice(cities), period=random.choice(periods))


