from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
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

    @action(detail=True, methods=['get'], url_path='weather-info')
    def weather_info(self, request, pk):
        query = get_object_or_404(CityModel, pk=pk)
        coords = get_city_coordinates(query.name)
        weather_info = get_city_weather(coords['lat'], coords['lon'])
        return Response(weather_info)


class PeriodViewSet(viewsets.ModelViewSet):
    serializer_class = PeriodSerializer
    queryset = PeriodModel.objects.all()

