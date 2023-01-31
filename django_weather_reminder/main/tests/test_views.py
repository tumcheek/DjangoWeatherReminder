from django.urls import reverse
from django_celery_beat.models import IntervalSchedule, PeriodicTask
from rest_framework.test import APITestCase
from rest_framework import status

from ..models import UserModel, CityModel, PeriodModel, SubscribersModel, \
    CountryModel


class TestUserApi(APITestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            "test@test.com", "trdsaf12", is_staff=True)
        self.city = CityModel.objects.create(name='Kyiv')
        self.country = CountryModel.objects.create(name='UA')
        self.period = PeriodModel.objects.create(period_of_notice=6)
        self.subscription = SubscribersModel.objects.create(
            user=self.user,
            city=self.city,
            country=self.country,
            period=self.period)
        self.subscription_info = {
            'email': self.user.email,
            'city': self.city.name,
            'country': self.country.name
        }
        self.interval = IntervalSchedule.objects.get_or_create(
            every=1, period=IntervalSchedule.HOURS,)
        self.periodic_task = PeriodicTask.objects.create(
            interval=self.interval[0],
            name=f'Subscriptions {self.subscription.pk}',
            task='main.end_weather_forecast_task',
            kwargs=self.subscription_info
        )
        self.users_url = reverse('main:usermodel-list')
        self.user_url = reverse(
            'main:usermodel-detail',
            kwargs={
                "pk": self.user.pk})
        self.subscriptions_url = reverse('main:subscriptions-list')
        self.subscription_url = reverse(
            'main:subscriptions-detail',
            kwargs={
                "pk": self.subscription.pk})
        self.cities_url = reverse('main:citymodel-list')
        self.city_url = reverse(
            'main:citymodel-detail',
            kwargs={
                "pk": self.city.pk})
        self.countries_url = reverse('main:countrymodel-list')
        self.country_url = reverse(
            'main:countrymodel-detail',
            kwargs={
                "pk": self.country.pk})
        self.periods_url = reverse('main:periodmodel-list')
        self.period_url = reverse(
            'main:periodmodel-detail',
            kwargs={
                "pk": self.period.pk})
        self.user_info = {"password": "rararawara", "email": "a@a.com"}
        self.subscription_info = {
            "user": self.user.pk,
            "city": self.city.pk,
            "country": self.country.pk,
            "period": self.period.pk}
        self.city_info = {"name": "Test"}
        self.country_info = {"name": "UA"}
        self.period_info = {"period_of_notice": 10}
        self.client.force_authenticate(self.user)

    def test_users_list_get(self):
        response = self.client.get(self.users_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_detail_get(self):
        response = self.client.get(self.user_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_detail_put(self):
        response = self.client.put(
            self.user_url,
            data=self.user_info,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_users_list_post(self):
        response = self.client.post(
            self.users_url,
            data=self.user_info,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_detail_delete(self):
        response = self.client.delete(self.user_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_subscriptions_list_get(self):
        response = self.client.get(self.subscriptions_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_subscription_detail_get(self):
        response = self.client.get(self.subscription_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_subscription_detail_put(self):
        response = self.client.put(
            self.subscription_url,
            data=self.subscription_info,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_subscriptions_list_post(self):
        response = self.client.post(
            self.subscriptions_url,
            data=self.subscription_info,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_subscription_detail_delete(self):
        response = self.client.delete(self.subscription_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_cities_list_get(self):
        response = self.client.get(self.cities_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cities_detail_get(self):
        response = self.client.get(self.city_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_city_detail_put(self):
        response = self.client.put(
            self.city_url,
            data=self.city_info,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cities_list_post(self):
        response = self.client.post(
            self.cities_url,
            data=self.city_info,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_city_detail_delete(self):
        response = self.client.delete(self.city_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_countries_list_get(self):
        response = self.client.get(self.countries_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_countries_detail_get(self):
        response = self.client.get(self.country_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_countries_detail_put(self):
        response = self.client.put(
            self.country_url,
            data=self.country_info,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_countries_list_post(self):
        response = self.client.post(
            self.countries_url,
            data=self.country_info,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_countries_detail_delete(self):
        response = self.client.delete(self.country_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_periods_list_get(self):
        response = self.client.get(self.periods_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_periods_detail_get(self):
        response = self.client.get(self.period_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_periods_detail_put(self):
        response = self.client.put(
            self.period_url,
            data=self.period_info,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_periods_list_post(self):
        response = self.client.post(
            self.periods_url,
            data=self.period_info,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_period_detail_delete(self):
        response = self.client.delete(self.period_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
