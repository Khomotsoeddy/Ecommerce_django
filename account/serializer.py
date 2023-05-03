from account.models import Address, Customer
from rest_framework import serializers

class CustomersSerializer(serializers.ModelSerializer):

    customer_id = serializers.CharField(source='id')

    class Meta:
        model = Customer
        fields = ('customer_id','password','last_login','is_superuser','email','name','id_number','date_of_birth','age_number','is_active','is_staff','gender','created','updated','mobile',"second_surname",'surname')

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('id','full_name','phone','postcode','address_line','address_line2','town_city','delivery_instructions','created_at','updated_at','default','customer_id')