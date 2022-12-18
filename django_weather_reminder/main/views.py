from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

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


class SubscribersViewSet(viewsets.ModelViewSet):
    serializer_class = SubscribersSerializer
    queryset = SubscribersModel.objects.all()

    @action(detail=True, methods=['get'], url_path='weather-info')
    def weather_info(self, request, pk):
        query = get_object_or_404(request.user.subscribersmodel_set, pk=pk)
        city = CityModel.objects.get(pk=query.city.pk)
        country = CityModel.objects.get(pk=query.country.pk)
        coords = get_city_coordinates(city.name, country.name)
        weather_info = get_city_weather(coords['lat'], coords['lon'])
        return Response(weather_info)

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list' or self.action == 'destroy':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsOwner | IsAdminUser]
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

