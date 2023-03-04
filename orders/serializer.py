from orders.models import Order, OrderItem
from rest_framework import serializers

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id','full_name','address1','address2','city','phone','created','updated','total_paid','order_key','billing_status','user_id','postal_code','country_code','email','payment_option')

class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id','price','order_id','product_id')