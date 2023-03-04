from django.urls import include, path
from rest_framework import routers

from . import views

app_name = "checkout"
router = routers.DefaultRouter()
router.register(r'delivery-options', views.DeliveryOptionsListView, basename='delivery_options')
router.register(r'payment-selections', views.PaymentSelectionsListView, basename='payment_selections')

urlpatterns = [
    path("deliverychoices", views.deliverychoices, name="deliverychoices"),
    path("basket_update_delivery/", views.basket_update_delivery, name="basket_update_delivery"),
    path("delivery_address/", views.delivery_address, name="delivery_address"),
    path("payment_selection/", views.payment_selection, name="payment_selection"),
    path("payment_complete/", views.payment_complete, name="payment_complete"),
    path("payment_successful/", views.payment_successful, name="payment_successful"),
    path('data/',include(router.urls))
]