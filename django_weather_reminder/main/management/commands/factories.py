import factory
from factory.django import DjangoModelFactory
from ...models import *


class UserFactory(DjangoModelFactory):
    class Meta:
        model = UserModel
    email = factory.Faker('email')


class CityFactory(DjangoModelFactory):
    class Meta:
        model = CityModel
    name = factory.Faker('city')


class PeriodFactory(DjangoModelFactory):
    class Meta:
        model = PeriodModel
    period_of_notice = factory.Faker('pyint')


class SubscribersFactory(DjangoModelFactory):
    class Meta:
        model = SubscribersModel

    user = factory.SubFactory(UserFactory)
    city = factory.SubFactory(CityFactory)
    period = factory.SubFactory(PeriodFactory)


