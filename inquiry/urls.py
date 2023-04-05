from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import routers

from inquiry import views

app_name = "inquiry"
router = routers.DefaultRouter()
router.register(r'inquiries', views.InquiryListView, basename='inquiries')

urlpatterns = [
    path('add_inquiry/', views.add_inquiry, name='add_inquiry'),
    path('data/',include(router.urls))
]
