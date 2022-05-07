from rest_framework import serializers
from .models import ConfirmationCode, Product

class ShippingSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    total = serializers.IntegerField()
    city = serializers.CharField()
    street = serializers.CharField()
    address = serializers.CharField()
    house = serializers.CharField()

class ProductSerializer(serializers.ModelSerializer):
    imageURL = serializers.ReadOnlyField()
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'actual_price',
            'is_availeble',
            'discount_price',
            'imageURL'
        ]


class ConfirmationCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfirmationCode
        fields = [ 
            'code',
            'name',
            'email',
            'amount'
        ]