from django.shortcuts import render
from rest_framework import viewsets
from inquiry.models import Inquiry
from inquiry.serializer import InquiriesSerializer

# Create your views here.
class InquiryListView(viewsets.ModelViewSet):
    serializer_class = InquiriesSerializer
    queryset = Inquiry.objects.all()

def add_inquiry(request):
    print('hiii')
    return render(request, 'store/home.html')

def delete(request):
    print('hiii')