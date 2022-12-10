from rest_framework import serializers

from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserModel.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
        )

        return user


class SubscribersSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscribersModel
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CityModel
        fields = '__all__'


class PeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodModel
        fields = '__all__'
