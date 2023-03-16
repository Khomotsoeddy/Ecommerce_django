import json
from account.models import Address
from basket.basket import Basket
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from checkout.serializer import DeliveryOptionsSerializer, PaymentSelectionsSerializer
from orders.models import Order, OrderDeliveryOption, OrderItem
from paypalcheckoutsdk.orders import OrdersGetRequest, OrdersCaptureRequest
from .paypal import PayPalClient
from rest_framework import viewsets
from .models import DeliveryOptions, PaymentSelections


@login_required
def deliverychoices(request):
    deliveryoptions = DeliveryOptions.objects.filter(is_active=True)
    return render(request, "checkout/delivery_choices.html", {"deliveryoptions": deliveryoptions})


@login_required
def basket_update_delivery(request):
    basket = Basket(request)
    if request.POST.get("action") == "post":
        delivery_option = int(request.POST.get("deliveryoption"))
        delivery_type = DeliveryOptions.objects.get(id=delivery_option)
        updated_total_price = basket.basket_update_delivery(delivery_type.delivery_price)

        session = request.session

        request.session['delivery_option'] = delivery_option
        if "purchase" not in request.session:
            session["purchase"] = {
                "delivery_id": delivery_type.id,
            }
        else:
            session["purchase"]["delivery_id"] = delivery_type.id
            session.modified = True

        response = JsonResponse({"total": updated_total_price, "delivery_price": delivery_type.delivery_price})
        return response


@login_required
def delivery_address(request):

    session = request.session
    if "purchase" not in request.session:
        messages.success(request, "Please select delivery option")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])

    addresses = Address.objects.filter(customer=request.user).order_by("-default")
    
    if len(addresses) ==0:
        return render(request, "account/dashboard/addresses.html")
    else:
        if "address" not in request.session:
            session["address"] = {"address_id": str(addresses[0].id)}
        else:
            session["address"]["address_id"] = str(addresses[0].id)
            session.modified = True
        
    return render(request, "checkout/delivery_address.html", {"addresses": addresses})


@login_required
def payment_selection(request):

    session = request.session
    if "address" not in request.session:
        messages.success(request, "Please select address option")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])
    
    shop = 'Shoprite'
    
    return render(request, "checkout/payment_selection.html", {'shop':shop})


####
# PayPay
####

@login_required
def payment_complete(request):
    PPClient = PayPalClient()
    

    body = json.loads(request.body)

    # print(body)
    data = body["orderID"]
    user_id = request.user.id

    # print(data,'',user_id)
    requestorder = OrdersGetRequest(data)
    # print(requestorder)
    response = PPClient.client.execute(requestorder)

    total_paid = response.result.purchase_units[0].amount.value
    basket = Basket(request)

    order = Order.objects.create(
        user_id=user_id,
        full_name=response.result.purchase_units[0].shipping.name.full_name,
        email=response.result.payer.email_address,
        address1=response.result.purchase_units[0].shipping.address.address_line_1,
        address2=response.result.purchase_units[0].shipping.address.admin_area_2,
        postal_code=response.result.purchase_units[0].shipping.address.postal_code,
        country_code=response.result.purchase_units[0].shipping.address.country_code,
        total_paid=response.result.purchase_units[0].amount.value,
        order_key=response.result.id,
        payment_option="paypal",
        billing_status=True,
    )
    print(order)
    order_id = order.pk

    delivery_option = request.session['delivery_option'] 

    OrderDeliveryOption.objects.create(order=order_id,delivery_option=delivery_option )
    for item in basket:
        print(item["product"])
        OrderItem.objects.create(order_id=order_id, product=item["product"], price=item["price"], quantity=item["qty"])

    return JsonResponse("Payment completed!", safe=False, )


@login_required
def payment_successful(request):
    basket = Basket(request)
    basket.clear()
    return render(request, "checkout/payment_successful.html", {})

class DeliveryOptionsListView(viewsets.ModelViewSet):
    serializer_class = DeliveryOptionsSerializer
    queryset = DeliveryOptions.objects.all()


class PaymentSelectionsListView(viewsets.ModelViewSet):
    serializer_class = PaymentSelectionsSerializer
    queryset = PaymentSelections.objects.all()
