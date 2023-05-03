from orders.models import Order, OrderDeliveryOption, OrderItem
from rest_framework import serializers

class OrderSerializer(serializers.ModelSerializer):

    order_id = serializers.CharField(source='id')
    class Meta:
        model = Order
        fields = ('order_id','full_name','address1','address2','city','phone','created','updated','total_paid','order_key','billing_status','user_id','postal_code','country_code','email','payment_option')

class OrderItemsSerializer(serializers.ModelSerializer):

    orderitem_id = serializers.CharField(source='id')
    class Meta:
        model = OrderItem
        fields = ('orderitem_id','price','order_id','product_id','quantity')

class OrderDeliveryOptionSerializer(serializers.ModelSerializer):

    orderdeliveryoption_id = serializers.CharField(source='id')
    order_id = serializers.CharField(source='order')
    class Meta:
        model = OrderDeliveryOption
        fields = ('orderdeliveryoption_id','delivery_option','order_id')