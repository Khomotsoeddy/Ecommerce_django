from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
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

        me = 'powerwm111@gmail.com'
        you = email
        subjectE = "Inquiry Confirmation"
        password = 'kddxamltpmiawtra'
        email_body = "<html><boby>"+"Hi "+name+"<br><br>Your inquery has successfully sent. We'll contact you soon<br><br><br>Regards<br>Mega Team"+"</body></html>"
        email_message = MIMEMultipart('alternative',None,[MIMEText(email_body, 'html')])

        email_message['subject'] = subjectE
        email_message['from'] = me
        email_message['to'] = email

        try:
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.ehlo()
            server.starttls()
            server.login(me,password)
            server.sendmail(me,you,email_message.as_string())
            print(email_message.as_string())
            server.quit()
        except Exception as e:
            print(f'error in sending email: {e}')
    
    return render(request, 'inquiry/inquiry.html')

def inqueries(request):
    inqueries = Inquiry.objects.all()
    return render(request, 'admin/query.html', {"inqueries": inqueries})

def delete(request):
    if request.POST.get('action') == 'post':
        inquiry_id = int(request.POST.get('inquiryid'))
        Inquiry.objects.filter(id = inquiry_id).delete()
    
    inqueries = Inquiry.objects.all()
    return render(request, 'admin/query.html', {"inqueries": inqueries})