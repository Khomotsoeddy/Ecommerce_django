from rest_framework import serializers
from store.models import Product

class productSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id','product_name','product_image','price','shop_retail','users_wishlist')