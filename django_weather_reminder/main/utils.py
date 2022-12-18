import requests
from django.conf import settings

WEATHER_API_KEY = getattr(settings, 'WEATHER_API_KEY')
GEO_URL = getattr(settings, 'GEO_URL')
WEATHER_URL = getattr(settings, 'WEATHER_URL')


def get_city_coordinates(city, country):
    city = city.replace(" ", "&")
    country = country.replace(" ", "&")
    req = requests.get(
        f'{GEO_URL}q={city,country}&limit=5&appid={WEATHER_API_KEY}')
    coordinates_dict = {
        'lat': req.json()[0]['lat'],
        'lon': req.json()[0]['lon'],
    }

    return coordinates_dict


def get_city_weather(lat, lon):
    units = 'units=metric'
    req = requests.get(
        f'{WEATHER_URL}lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&{units}'
    )
    return req.json()



