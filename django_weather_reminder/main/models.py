from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class UserModel(AbstractUser):
    username = None
    first_name = None
    last_name = None
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class CityModel(models.Model):
    name = models.CharField(max_length=255)


class PeriodModel(models.Model):
    period_of_notice = models.IntegerField()


class SubscribersModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    city = models.ForeignKey(CityModel, on_delete=models.CASCADE)
    period = models.ForeignKey(PeriodModel, on_delete=models.CASCADE)
