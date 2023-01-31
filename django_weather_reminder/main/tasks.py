from celery import shared_task, chain
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

from .utils import get_city_coordinates, get_city_weather
from .models import EmailSubjectModel


@shared_task(ignore_result=True)
def get_city_coordinates_task(city: str, country: str) -> dict:
    return get_city_coordinates(city, country)


@shared_task(ignore_result=True)
def get_city_weather_task(coordinates: dict) -> dict:
    if not isinstance(coordinates, dict):
        raise TypeError('Parameter of function must be a dict')
    try:
        lat, lon = coordinates['lat'], coordinates['lon']
    except KeyError:
        raise KeyError('Your dict should have "lat" and "lan" keys')
    return get_city_weather(lat, lon)


@shared_task
def send_mail_task(
        weather_info: dict,
        email: str,
        city: str,
        country: str) -> None:
    mail_subject = EmailSubjectModel.objects.all()[0].subject_text
    context = {
        'city': city,
        'country': country,
        'description': weather_info["weather"][0]["description"],
        'temp': weather_info["main"]["temp"],
        'feels_like': weather_info["main"]["feels_like"],
        'temp_min': weather_info["main"]["temp_min"],
        'temp_max': weather_info["main"]["temp_max"],
        'wind_speed': weather_info["wind"]["speed"]
    }
    message = render_to_string(
        'main/email_message.html',
        context=context
    )
    try:
        from_email = getattr(settings, 'EMAIL_HOST_USER')
    except AttributeError:
        raise AttributeError(
            'You must add EMAIL_HOST_USER attribute to your settings')
    send_mail(
        subject=mail_subject,
        message=message,
        from_email=from_email,
        recipient_list=[email],
        fail_silently=True,
    )


@shared_task
def send_weather_forecast_task(email: str, city: str, country: str) -> None:
    weather_info = chain(
        get_city_coordinates_task.s(
            city, country) | get_city_weather_task.s() | send_mail_task.s(
            email, city, country))
    weather_info.apply_async()
