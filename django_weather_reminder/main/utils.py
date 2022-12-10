import requests
from django.conf import settings

WEATHER_API_KEY = getattr(settings, 'WEATHER_API_KEY')


def get_city_coordinates(city):
    req = requests.get(
        f'https://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={WEATHER_API_KEY}')
    coordinates_dict = {
        'lat': req.json()[0]['lat'],
        'lon': req.json()[0]['lon'],
    }

    return coordinates_dict


def get_city_weather(lat, lon):
    req = requests.get(
        f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric'
    )
    return req.json()



