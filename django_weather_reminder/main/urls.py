from django.urls import path
from .views import *
from rest_framework import routers


app_name = 'main'
router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'cities', CityViewSet)
router.register(r'countries', CountryViewSet)
router.register(r'periods', PeriodViewSet)

urlpatterns = [
    path('subscriptions/<int:pk>/', SubscriptionAPIView.as_view(), name='subscriptions-detail'),
    path('subscriptions/', SubscriptionAPIView.as_view(), name='subscriptions-list'),
]
urlpatterns += router.urls
