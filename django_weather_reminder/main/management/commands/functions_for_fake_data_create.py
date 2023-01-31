import random

from .factories import *
from ...models import *
from faker import Faker


def delete_all_data():
    UserModel.objects.all().delete()
    CityModel.objects.all().delete()
    CountryModel.objects.all().delete()
    PeriodModel.objects.all().delete()
    SubscribersModel.objects.all().delete()


def create_fake_users(num_users, password):
    people = []
    for _ in range(num_users):
        person = UserFactory(password=password)
        people.append(person)
    return people


def create_fake_cities(num_cities, country):
    cities = []
    for _ in range(num_cities):
        city = CityFactory(name=Faker(country).city_name())
        cities.append(city)
    return cities


def create_fake_countries(countries_list_code):
    countries = []
    for code in countries_list_code:
        country = CountryFactory(name=code)
        countries.append(country)
    return countries


def create_fake_periods(periods_list):
    periods = []
    for _period in periods_list:
        period = PeriodFactory(period_of_notice=_period)
        periods.append(period)
    return periods


def create_fake_subscribers(num_subscribers, people, cities, countries, periods):
    for _ in range(num_subscribers):
        SubscribersFactory(user=random.choice(people), city=random.choice(cities), country=random.choice(countries),
                           period=random.choice(periods))


