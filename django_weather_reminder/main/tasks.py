from celery import shared_task, chain
from celery.result import allow_join_result
from django.core.mail import send_mail
from django.conf import settings

from .utils import get_city_coordinates, get_city_weather, create_message


@shared_task
def get_city_coordinates_task(city, country):
    return get_city_coordinates(city, country)


@shared_task
def get_city_weather_task(coordinates):
    lat, lon = coordinates['lat'], coordinates['lon']
    return get_city_weather(lat, lon)


@shared_task
def send_mail_task(email, city, country):
    mail_subject = "Weather forecast"
    with allow_join_result():
        weather_info = chain(get_city_coordinates_task.s(city, country) | get_city_weather_task.s())().get()
        message = create_message(weather_info, city, country)
        send_mail(
            subject=mail_subject,
            message=message,
            from_email=getattr(settings, 'EMAIL_HOST_USER'),
            recipient_list=[email],
            fail_silently=True,
        )

    return "Done"

