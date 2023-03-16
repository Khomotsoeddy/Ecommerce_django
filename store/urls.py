from django.urls import path

from store import views

app_name = 'store'

urlpatterns = [
    path('', views.home, name='home'),
    path('products', views.product_all, name='store_home'),
    path('<slug:id>', views.product_detail, name='product_detail'),
]
