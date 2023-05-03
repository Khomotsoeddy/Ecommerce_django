from rest_framework import serializers
from store.models import Product

class productSerializer(serializers.ModelSerializer):

    product_id = serializers.CharField(source='id')
    class Meta:
        model = Product
        fields = ('product_id','product_name','product_image','price','shop_retail','users_wishlist')