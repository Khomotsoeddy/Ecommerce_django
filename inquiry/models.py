from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class Inquiry(models.Model):
    email = models.EmailField(max_length=254)
    mobile = PhoneNumberField(blank=True)
    message = models.TextField()
