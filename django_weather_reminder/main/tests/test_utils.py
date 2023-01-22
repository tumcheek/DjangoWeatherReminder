from unittest import TestCase
from unittest.mock import patch

from ..utils import get_city_coordinates, get_city_weather


class TestTasks(TestCase):
    def setUp(self):
        self.test_data = [{'lat': 1, 'lon': 2}]
        self.result = {'lat': 1, 'lon': 2}

        class MockResponse:
            def __init__(self, json_data):
                self.json_data = json_data

            def json(self):
                return self.json_data

        self.response = MockResponse(self.test_data)

    def test_get_city_coordinates(self):
        with patch('requests.get', return_value=self.response):
            result = get_city_coordinates('test', 'test')
            self.assertEqual(result, self.result)

    def test_get_get_city_weather(self):
        with patch('requests.get', return_value=self.response):
            result = get_city_weather('test', 'test')
            self.assertEqual(result, self.test_data)
