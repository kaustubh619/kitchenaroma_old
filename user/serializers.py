from rest_framework import serializers
from .models import CustomUser


class UserLocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['user_location_latitude', 'user_location_longitude', 'gmap_address']