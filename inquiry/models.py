import django
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class Inquiry(models.Model):
    name = models.CharField(null=False, max_length=200)
    email = models.EmailField(max_length=254)
    mobile = PhoneNumberField(blank=True)
    subject = models.CharField(null=False, max_length=100)
    message = models.TextField()
    created = models.DateTimeField(default=django.utils.timezone.now)
