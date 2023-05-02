from django.urls import include, path
from rest_framework import routers
from store import views

app_name = 'store'
router = routers.DefaultRouter()
router.register(r'product', views.ProductListView, basename='my-products')

urlpatterns = [
    path('', views.home, name='home'),
    path('products', views.product_all, name='store_home'),
    path('sort-products', views.sorting_product, name='sort_products'),
    path('get_data', views.get_data, name='get_data'),
    path('<slug:id>', views.product_detail, name='product_detail'),
    path('data/',include(router.urls)),
    # path('product', views.search_product, name='product')
]
