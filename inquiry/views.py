from django.shortcuts import render
from rest_framework import viewsets
from inquiry.models import Inquiry
from inquiry.serializer import InquiriesSerializer

# Create your views here.
class InquiryListView(viewsets.ModelViewSet):
    serializer_class = InquiriesSerializer
    queryset = Inquiry.objects.all()

def add_inquiry(request):
    print(request.method)
    if request.method == 'POST':
        name = request.POST["name"]
        email = request.POST["email"]
        mobile= request.POST["mobile"]
        subject = request.POST["subject"]
        message= request.POST["message"]
        i = Inquiry(name=name,email=email,mobile=mobile,subject=subject,message=message)
        i.save()
    return render(request, 'inquiry/inquiry.html')

def delete(request):
    print('hiii')