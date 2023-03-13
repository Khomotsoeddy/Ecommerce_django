from account.models import Address, Customer
from rest_framework import serializers

class CustomersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id','password','last_login','is_superuser','email','name','mobile','id_number','age_number','gender','is_active','created','updated')

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('id','full_name','phone','postcode','address_line','address_line2','town_city','delivery_instructions','created_at','updated_at','default','customer_id')