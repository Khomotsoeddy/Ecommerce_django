from django.urls import path

from store import views

app_name = 'store'

urlpatterns = [
    path('', views.home, name='home'),
    path('products', views.product_all, name='store_home'),
    path('get_data', views.get_data, name='get_data'),
    path('<slug:id>', views.product_detail, name='product_detail'),
    # path('product', views.search_product, name='product')
]
