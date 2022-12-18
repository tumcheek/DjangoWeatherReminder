from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager


class UserModel(AbstractUser):
    username = None
    first_name = None
    last_name = None
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()


class CityModel(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class CountryModel(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class PeriodModel(models.Model):
    period_of_notice = models.IntegerField()

    def __str__(self):
        return str(self.period_of_notice)


class SubscribersModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    city = models.ForeignKey(CityModel, on_delete=models.CASCADE)
    country = models.ForeignKey(CountryModel, on_delete=models.CASCADE)
    period = models.ForeignKey(PeriodModel, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)