from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from account.serializer import AddressSerializer, CustomersSerializer
from checkout.models import DeliveryOptions
from rest_framework import viewsets
from orders.models import Order, OrderDeliveryOption
from orders.views import user_orders
from store.models import Product
import re
import calendar
from datetime import date, datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib 

from .forms import RegistrationForm, UserAddressForm, UserEditForm
from .models import Address, Customer
from .tokens import account_activation_token


@login_required
def wishlist(request):
    products = Product.objects.filter(users_wishlist=request.user)
    return render(request, "account/dashboard/user_wish_list.html", {"wishlist": products})


@login_required
def add_to_wishlist(request, id):
    product = get_object_or_404(Product, id=id)
    if product.users_wishlist.filter(id=request.user.id).exists():
        product.users_wishlist.remove(request.user)
        messages.success(request, product.product_name + " has been removed from your WishList")
    else:
        product.users_wishlist.add(request.user)
        messages.success(request, "Added " + product.product_name + " to your WishList")
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


@login_required
def dashboard(request):
    orders = user_orders(request)
    return render(request, "account/dashboard/dashboard.html", {"section": "profile", "orders": orders})

@login_required
def delete_user(request):

    user = Customer.objects.get(id=request.user.id)
    user.is_active = False
    user.delete()
    logout(request)
    return redirect("account:delete_confirmation")


def account_register(request):

    if request.user.is_authenticated:
        return redirect("account:dashboard")

    if request.method == "POST":
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data["email"]
            user.set_password(registerForm.cleaned_data["password"])
            user.mobile = registerForm.cleaned_data['mobile']
            user.id_number = registerForm.cleaned_data['id_number']
            
            user_id = user.id_number

            year = int(user_id[0:2])
            month = int(user_id[2:4])

            day = int(user_id[4:6])

            current_year = datetime.now().year

            if year < 22: 
                year += 2000
            else:
                year += 1900
            
            birthdate= date(year,month,day)

            age = current_year - year

            gender_digit = int(user_id[6])
            gender = 'Male' if gender_digit >= 5 else 'Female'

            user.date_of_birth = birthdate
            user.	age_number = age
            user.gender = gender
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = "Activate your Account"
            message = render_to_string(
                "account/registration/account_activation_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            
            me = 'powerwm111@gmail.com'
            you = user.email
            password = 'kddxamltpmiawtra'
            email_body = "<html><boby>"+"Hi "+user.name+"\n\nYour account has successfully created. Please click below link to activate your account\n\n\n"+'http://'+current_site.domain+'/account/activate/'+urlsafe_base64_encode(force_bytes(user.pk))+'/'+account_activation_token.make_token(user)+"\n\nRegards\nMega Team"+"</body></html>"
            email_message = MIMEMultipart('alternative',None,[MIMEText(email_body, 'html')])

            email_message['subject'] = subject
            email_message['from'] = me
            email_message['to'] = user.email

            try:
                server = smtplib.SMTP('smtp.gmail.com:587')
                server.ehlo()
                server.starttls()
                server.login(me,password)
                server.sendmail(me,you,email_message.as_string())
                server.quit()
            except Exception as e:
                print(f'error in sending email: {e}')

            user.email_user(subject=subject, message=message)
            return render(request, "account/registration/register_email_confirm.html", {"form": registerForm})
    else:
        registerForm = RegistrationForm()
    return render(request, "account/registration/register.html", {"form": registerForm})


def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Customer.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect("account:dashboard")
    else:
        return render(request, "account/registration/activation_invalid.html")


# Addresses


@login_required
def view_address(request):
    addresses = Address.objects.filter(customer=request.user)
    return render(request, "account/dashboard/addresses.html", {"addresses": addresses})


@login_required
def add_address(request):
    if request.method == "POST":
        address_form = UserAddressForm(data=request.POST)
        if address_form.is_valid():
            address_form = address_form.save(commit=False)
            address_form.customer = request.user
            address_form.save()
            return HttpResponseRedirect(reverse("account:addresses"))
    else:
        address_form = UserAddressForm()
    return render(request, "account/dashboard/edit_addresses.html", {"form": address_form})

@login_required
def edit_details(request):
    if request.method == "POST":

        user = Customer.objects.get(id=request.user.id)
        
        user.name = request.POST['name']
        mobile = request.POST['mobile']

        if(len(mobile) != 12):
            messages.error(request, 'Incorrect number, record is not updated!!')
        else:
            pattern=r"[+27][^.......$]"  
            match = re.match(pattern,mobile) 
            if not match:
                messages.error(request, 'Incorrect number format, record is not updated!!')
            else:
                user.mobile = mobile
                user.save()
        # user_form = UserEditForm(instance=user, data=request.POST)
        user_form = UserEditForm(instance=user)
        print(user_form.is_valid())
        if user_form.is_valid():
            # user_form.name = request.POST['name']
            # user_form.mobile = request.POST['mobile']
            print('saved')
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)

    return render(request, "account/dashboard/edit_details.html", {"user_form": user_form})

@login_required
def edit_address(request, id):
    if request.method == "POST":
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserAddressForm(instance=address, data=request.POST)
        if address_form.is_valid():
            address_form.save()
            return HttpResponseRedirect(reverse("account:addresses"))
    else:
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserAddressForm(instance=address)
    return render(request, "account/dashboard/edit_addresses.html", {"form": address_form})


@login_required
def delete_address(request, id):
    address = Address.objects.filter(pk=id, customer=request.user).delete()
    return redirect("account:addresses")


@login_required
def set_default(request, id):
    Address.objects.filter(customer=request.user, default=True).update(default=False)
    Address.objects.filter(pk=id, customer=request.user).update(default=True)

    previous_url = request.META.get("HTTP_REFERER")

    if "delivery_address" in previous_url:
        return redirect("checkout:delivery_address")

    return redirect("account:addresses")


@login_required
def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    print(orders)
    return render(request, "account/dashboard/user_orders.html", {"orders": orders})

def order_detail(request):
    user_id = request.user.id

    order_id = request.GET['order_id']

    option = OrderDeliveryOption.objects.filter(order=order_id[0])
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True).filter(id=order_id[0])
    for op in option:
        delivery_option = DeliveryOptions.objects.filter(id=op.delivery_option)
        print(delivery_option)
    
    
    return render(request, "account/dashboard/order_detail.html",{"orders": orders, 'delivery_option':delivery_option})

class CustomersListView(viewsets.ModelViewSet):
    serializer_class = CustomersSerializer
    queryset = Customer.objects.all()


class AddressListView(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()