from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets
from basket.basket import Basket
from orders.serializer import OrderItemsSerializer, OrderSerializer

from .models import Order, OrderItem


def add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':

        order_key = request.POST.get('order_key')
        user_id = request.user.id
        baskettotal = basket.get_total_price()

        # Check if order exists
        if Order.objects.filter(order_key=order_key).exists():
            pass
        else:
            order = Order.objects.create(user_id=user_id, full_name='name', address1='add1',
                                address2='add2', total_paid=baskettotal, order_key=order_key)
            order_id = order.pk

            for item in basket:
                print(item)
                OrderItem.objects.create(order_id=order_id, product=item['product'], price=item['price'], quantity=item['qty'])

        response = JsonResponse({'success': 'Return something'})
        return response


def payment_confirmation(data):
    Order.objects.filter(order_key=data).update(billing_status=True)


def user_orders(request):
    orders = Order.objects.all()

    print(orders)
    return orders
    

def admin_orders(request):
    orders = Order.objects.all()

    print(orders)
    return render(request, "admin/orders.html", {"orders": orders})

class OrdersListView(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


class OrderItemsListView(viewsets.ModelViewSet):
    serializer_class = OrderItemsSerializer
    queryset = OrderItem.objects.all()
