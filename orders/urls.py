from django.urls import include, path
from rest_framework import routers
from orders import views

app_name = 'orders'
router = routers.DefaultRouter()
router.register(r'orders', views.OrdersListView, basename='orders')
router.register(r'order-items', views.OrderItemsListView, basename='order-items')
router.register(r'OrderDeliveryOption', views.OrderDeliveryOptionList, basename='OrderDeliveryOption')

urlpatterns = [
    path('add/', views.add, name='add'),
    path('my-orders', views.user_orders, name='my-orders'),
    path('orders', views.admin_orders, name='orders'),
    path('data/',include(router.urls)),
    path('download-txt/', views.download_txt, name='download_txt'),
    path('admin_orders_report/', views.admin_orders_report, name="admin_orders_report"),
    path('overall_summary/', views.overall_summary, name='overall_summary'),
    path('filter_admin_orders_by_date', views.filter_admin_orders_by_date, name="filter_admin_orders_by_date")
]
