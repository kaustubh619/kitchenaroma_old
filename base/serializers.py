from rest_framework import serializers
from .models import Cart, Kitchen, Timing, Order


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
        depth = 3


class KitchenNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Kitchen
        fields = '__all__'


class TimingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Timing
        fields = '__all__'


class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'        



