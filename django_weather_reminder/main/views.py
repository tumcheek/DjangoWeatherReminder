import json

from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from django_celery_beat.models import IntervalSchedule, PeriodicTask

from .models import *
from .serializers import *
from .utils import *
from .permissions import *


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list' or self.action == 'destroy':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsUser | IsAdminUser]
        return [permission() for permission in permission_classes]


class CityViewSet(viewsets.ModelViewSet):
    serializer_class = CitySerializer
    queryset = CityModel.objects.all()


class CountryViewSet(viewsets.ModelViewSet):
    serializer_class = CountrySerializer
    queryset = CountryModel.objects.all()


class PeriodViewSet(viewsets.ModelViewSet):
    serializer_class = PeriodSerializer
    queryset = PeriodModel.objects.all()


class SubscriptionAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            subscriptions = get_object_or_404(
                SubscribersModel, user=request.user.pk, pk=pk)
            return Response(
                SubscribersSerializer(
                    subscriptions,
                    many=False).data)
        else:
            subscriptions = SubscribersModel.objects.filter(
                user=request.user.pk)
            return Response(
                SubscribersSerializer(
                    subscriptions,
                    many=True).data)

    def post(self, request):
        serializer = SubscribersSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        hours = PeriodModel.objects.get(pk=serializer.data.get("period"))
        interval, created = IntervalSchedule.objects.get_or_create(
            every=hours, period=IntervalSchedule.HOURS,)
        email = UserModel.objects.get(pk=serializer.data.get("user")).email
        city = CityModel.objects.get(pk=serializer.data.get("city")).name
        country = CountryModel.objects.get(
            pk=serializer.data.get("country")).name
        subscription_info = json.dumps({
            'email': email,
            'city': city,
            'country': country
        })
        PeriodicTask.objects.create(
            interval=interval,
            name=f'Subscriptions {serializer.data.get("id")}',
            task='main.end_weather_forecast_task',
            kwargs=subscription_info
        )
        return Response(serializer.data, 201)

    def put(self, request, pk):
        instance = get_object_or_404(SubscribersModel, pk=pk)
        serializer = SubscribersSerializer(
            data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        hours = PeriodModel.objects.get(pk=serializer.data.get("period"))
        interval, created = IntervalSchedule.objects.get_or_create(
            every=hours, period=IntervalSchedule.HOURS, )
        email = UserModel.objects.get(pk=serializer.data.get("user")).email
        city = CityModel.objects.get(pk=serializer.data.get("city")).name
        country = CountryModel.objects.get(
            pk=serializer.data.get("country")).name
        subscription_info = json.dumps({
            'email': email,
            'city': city,
            'country': country
        })
        task = PeriodicTask.objects.get(name=f"Subscriptions {pk}")
        task.interval = interval
        task.kwargs = subscription_info
        task.save()

        return Response(serializer.data)

    def delete(self, request, pk):
        user_pk = request.user.pk
        subscription = get_object_or_404(SubscribersModel, pk=pk, user=user_pk)
        subscription.delete()
        PeriodicTask.objects.get(name=f"Subscriptions {pk}").delete()
        return Response({"delete": "ok"}, 204)
