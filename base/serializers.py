from rest_framework import serializers
from .models import Cart, Kitchen


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = "__all__"


class KitchenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Kitchen
        fields = ['gmap_address', 'kitchen_latitude', 'kitchen_longitude']


class CartSerializerWithDepth(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = "__all__"
        depth = 1



