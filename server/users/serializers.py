from rest_framework import serializers
from .models import *


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = DistrictModel
        fields = ['name']


class DistrictDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DistrictModel
        fields = ['pk', 'name']

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = DistrictModel
        fields = ['name']

class CityDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DistrictModel
        fields = ['pk', 'name']


class UserLoginSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(max_length=20)
    telegram_id = serializers.CharField(max_length=30)
    
    class Meta:
        model = UserModel
        fields = ['phone', 'telegram_id']

    def validate(self, value):
        if not UserModel.objects.filter(phone=value).exists():
            return value
        return value


class UserMeSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    city = CityDetailSerializer()
    district = DistrictDetailSerializer()
    long = serializers.IntegerField(required=False)
    lat = serializers.IntegerField(required=False)
    
    class Meta:
        model = UserModel
        fields = ['id', 'phone', 'telegram_id', 'avatar', 'first_name', 'district', 'city', 'address', 'long', 'lat', 'date_joined', 'is_active']
        depth = 1

    def get_avatar(self, obj):
        return f"api/{obj.avatar}"
    
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['phone', 'first_name', 'avatar', 'district', 'city', 'address', 'longt', 'lat']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id', 'phone', 'first_name', 'avatar', 'address']
