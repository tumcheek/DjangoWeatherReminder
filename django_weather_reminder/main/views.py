from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializers import *
from .utils import *


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer


class SubscribersViewSet(viewsets.ModelViewSet):
    serializer_class = SubscribersSerializer
    queryset = SubscribersModel.objects.all()


class CityViewSet(viewsets.ModelViewSet):
    serializer_class = CitySerializer
    queryset = CityModel.objects.all()


class PeriodViewSet(viewsets.ModelViewSet):
    serializer_class = PeriodSerializer
    queryset = PeriodModel.objects.all()


class CitiAPIView(APIView):
    def get(self, request, city_name):
        coords = get_city_coordinates(city_name)
        weather_info = get_city_weather(coords['lat'], coords['lon'])
        return Response(weather_info)
