from django.urls import path
from .views import *
from rest_framework import routers


app_name = 'main'
router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'subscriptions', SubscribersViewSet)
router.register(r'cities', CityViewSet)
router.register(r'countries', CountryViewSet)
router.register(r'periods', PeriodViewSet)

urlpatterns = router.urls
