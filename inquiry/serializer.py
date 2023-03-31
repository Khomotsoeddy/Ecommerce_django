from inquiry.models import Inquiry
from rest_framework import serializers


class InquiriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = ('id','name','email','mobile','subject','message','created')