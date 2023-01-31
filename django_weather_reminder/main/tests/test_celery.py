from unittest.mock import patch
from django.test import TestCase

from ..tasks import get_city_coordinates_task, get_city_weather_task, send_mail_task, send_weather_forecast_task


class TestTasks(TestCase):
    def setUp(self):
        self.test_coordinates = {'lat': 1, 'lon': 2}
        self.test_weather_info = {
            'weather':
                [
                    {
                        'description': 'test',
                    }
                ],
            'main': {
                'temp': 1,
                'feels_like': 1,
                'temp_min': 1,
                'temp_max': 2,
                    },
            'wind': {
                'speed': 1.1
                    }

        }
        self.test_mail = 'test@test.com'

    def test_get_coordinates(self):
        with patch('main.tasks.get_city_coordinates', return_value=self.test_coordinates):
            result = get_city_coordinates_task.delay('test', 'test')
            self.assertEqual(result.get(), self.test_coordinates)
            self.assertTrue(result.successful())

    def test_get_city_weather(self):
        with patch('main.tasks.get_city_weather', return_value=self.test_weather_info):
            result = get_city_weather_task.delay(self.test_coordinates)
            self.assertEqual(result.get(), self.test_weather_info)
            self.assertTrue(result.successful())

    def test_send_mail(self):
        result = send_mail_task.delay(
            self.test_weather_info, self.test_mail, 'test', 'test')
        self.assertTrue(result.successful())

    def test_send_weather_forecast(self):
        with patch('main.tasks.get_city_coordinates', return_value=self.test_coordinates):
            with patch('main.tasks.get_city_weather', return_value=self.test_weather_info):
                result = send_weather_forecast_task.delay(
                    self.test_mail, 'test', 'test')
                self.assertTrue(result.successful())
