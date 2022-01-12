from rest_framework import serializers

class ShippingSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    total = serializers.IntegerField()
    city = serializers.CharField()
    street = serializers.CharField()
    address = serializers.CharField()
    house = serializers.CharField()
