from checkout.models import DeliveryOptions, PaymentSelections
from rest_framework import serializers

class DeliveryOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryOptions
        fields = ('id','delivery_name','delivery_price','delivery_timeframe','delivery_window','order','is_active')

class PaymentSelectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentSelections
        fields = ('id','name','is_active')