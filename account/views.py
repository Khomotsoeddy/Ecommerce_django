import logging as logger
from django.contrib import messages
from django.contrib.auth import login, logout,authenticate
from django.db.models import Q, F
from django.db.models import Value as V
import re
from django.db.models.functions import Concat
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
from inquiry.models import Inquiry
from orders.models import Order, OrderDeliveryOption
from orders.views import user_orders
from store.models import Product
from datetime import date, datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib 
from dateutil.parser import parse
import string
from .forms import LoginForm, RegistrationForm, UserAddressForm, UserEditForm, UserLoginForm
from .models import Address, Customer
from .tokens import account_activation_token
from fpdf import FPDF
import xlwt
from django.http import HttpResponse
from django.contrib.messages import get_messages
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if Customer.objects.filter(email=username).exists():
                if Customer.objects.filter(email=username).filter(is_active=False).exists():
                    messages.error(request, 'Your account is not active')
                else:
                    user = authenticate(request, username=username, password=password)
                    if user is not None:
                        login(request, user)
                        return redirect('account:dashboard')
                    else:
                        messages.error(request, 'Invalid password.')
            else:
                # User does not exist
                messages.error(request, 'User does not exist.')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

@login_required
def delete_customer(request):
    if request.POST.get('action') == 'post':
        customer_id = int(request.POST.get('customerid'))
        customer = Customer.objects.filter(id = customer_id)

        print("========> they are removing me",customer)

        customer.delete()

    customers = Customer.objects.filter(is_staff=False)
    return render(request, "admin/customers.html",{"customers":customers} )

@login_required
def deactivate_user(request):
    if request.POST.get('action') == 'post':
        customer_id = int(request.POST.get('customerid'))
        customer = Customer.objects.get(id = customer_id)

        customer.is_active = False
        customer.save()

        print("========> they are deactivating me",customer)
    customers = Customer.objects.filter(is_staff=False)
    return render(request, "admin/customers.html",{"customers":customers} )

@login_required
def activate_user(request):
    if request.POST.get('action') == 'post':
        customer_id = int(request.POST.get('customerid'))
        customer = Customer.objects.get(id = customer_id)

        customer.is_active = True
        customer.save()
        print("========> they are activating me",customer)

    customers = Customer.objects.filter(is_staff=False)
    return render(request, "admin/customers.html",{"customers":customers} )

@login_required
def download_all_customer_excel(request):
    print('============> im here')
    response = HttpResponse(content_type = 'application/ms-excel')

    response['Content-Disposition'] = 'attachment; filename="Customers.xls"'

    wb = xlwt.Workbook(encoding = 'utf-8')

    ws = wb.add_sheet('customers')

    row_num = 0

    font_style = xlwt.XFStyle()

    font_style.font.bold = True

    columns = ['id','name','surname','second surname',
               'email','mobile','ID number','Date of Birth',
               'Age','Is Active','Created On','Gender']

    for col_num  in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    customers = Customer.objects.filter(is_staff=False).values_list(
        'id','name','surname','second_surname','email','mobile','id_number','date_of_birth','age_number','is_active','created','gender')
    
    customers =[[x.strftime("%Y-%m-%d %H:%M") if isinstance(x, datetime) else x for x in row] for row in customers ]
    customers = [[x.strftime("%Y-%m-%d") if isinstance(x, date) else x for x in row]  for row in customers]
    for row in customers:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


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

    cust_cont = Customer.objects.all().count()
    prop_cont =  Product.objects.all().count()
    ord_cont = Order.objects.all().count()
    quer_cont = Inquiry.objects.all().count()

    return render(request, "account/dashboard/dashboard.html", {"section": "profile", "orders": orders, 'cust_total':cust_cont, 'prop_cont':prop_cont, 'ord_cont': ord_cont,"quer_cont":quer_cont})

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
        try:    
            registerForm = RegistrationForm(request.POST)
            if registerForm.is_valid():
                user = registerForm.save(commit=False)
                user.email = registerForm.cleaned_data["email"]
                user.set_password(registerForm.cleaned_data["password"])
                user.mobile = registerForm.cleaned_data['mobile']
                user.id_number = registerForm.cleaned_data['id_number']
                user.name = registerForm.cleaned_data['name']
                user.second_surname = registerForm.cleaned_data['second_surname']
                user.surname = registerForm.cleaned_data['surname']
                
                user_id = user.id_number

                year = int(user_id[0:2])
                month = int(user_id[2:4])
                day = int(user_id[4:6])

                current_year = datetime.now().year

                if year < 22: 
                    year += 2000
                else:
                    year += 1900

                age = current_year - year

                if age >= 18 :

                    gender_digit = int(user_id[6])
                    gender = 'Male' if gender_digit >= 5 else 'Female'

                    user.age_number = age
                    user.gender = gender
                    birthdate= date(year,month,day)
                    user.date_of_birth = birthdate
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
                    email_body = "<html><boby>"+"Hi "+user.name+"<br><br>Your account has successfully created. Please click below link to activate your account<br><br>"+'http://'+current_site.domain+'/account/activate/'+urlsafe_base64_encode(force_bytes(user.pk))+'/'+account_activation_token.make_token(user)+"<br><br>Regards<br>Mega Team"+"</body></html>"
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
                        print(email_message.as_string())
                        server.quit()
                    except Exception as e:
                        print(f'error in sending email: {e}')

                    user.email_user(subject=subject, message=message)
                    return render(request, "account/registration/register_email_confirm.html", {"form": registerForm})
                else:
                    messages.error(request, 'Person under the age of 18 are not allowed to register')
                # try:
        except Exception as e:
            print('---------------->',e)
            messages.error(request, 'Invalid ID number')
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
        print('this side')
        return redirect("account:dashboard")
    else:
        return render(request, "account/registration/activation_invalid.html")

@login_required
def DownloadSammary(request):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size = 15)

    pdf.cell(200, 10, txt = "GeeksforGeeks",
         ln = 1, align = 'C')
    
    pdf.cell(200, 10, txt = "A Computer Science portal for geeks.",
         ln = 2, align = 'C')
    pdf.output("order.pdf")

@login_required
def get_customers(request):
    if request.method == "POST":
        deta =  request.POST['search_data']
        print("---------->",deta)
        if deta == "":
            print("nothing")
            messages.error(request, 'Please insert something')
        else:
            customers = Customer.objects.annotate(full_name=Concat('name', V(" "), 'surname')).annotate(full_name_second=Concat('name', V(" "), 'surname', V(' '), 'second_surname')).filter(Q(full_name_second=deta)|Q(full_name=deta) | Q(name__contains=deta) | Q(surname__contains=deta) | Q(second_surname__contains=deta)).filter(is_staff=False)
            return render(request, "admin/customers.html",{"customers":customers} )

    customers = Customer.objects.filter(is_staff=False)
    return render(request, "admin/customers.html",{"customers":customers} )

@login_required
def customer_detail(request, id):

    orders = Order.objects.filter(user_id = id)
    customer = get_object_or_404(Customer.objects.all().filter(id=id))
    print(customer.id)
    return render(request, "admin/customer-detail.html",{"customer":customer, 'orders':orders})

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
            address = address_form.save(commit=False)
            address.full_name = address_form.cleaned_data["full_name"]
            address.postcode = address_form.cleaned_data["postcode"]
            counter = len(re.findall(r'\d', address.full_name))
            if counter > 0:
                messages.error(request, 'Enter valid name')
            if not address.postcode.isdigit() or len(address.postcode) != 4 :
                messages.error(request, 'Enter valid postal code')

            storage = get_messages(request)
            if len(storage) == 0:
                address.customer = request.user
                address.save()
                return HttpResponseRedirect(reverse("account:addresses"))
    else:
        address_form = UserAddressForm()
    return render(request, "account/dashboard/edit_addresses.html", {"form": address_form})

@login_required
def edit_details(request):
    if request.method == "POST":

        user = Customer.objects.get(id=request.user.id)
        
        user.name = request.POST['name']
        user.surname = request.POST['surname']
        mobile = request.POST['mobile']

        if(len(mobile) != 12):
            messages.error(request, 'Incorrect number, record is not updated!!')
        else:
            pattern=r"[+27][^.......$]"  
            match = re.match(pattern,mobile) 
            if not match:
                messages.error(request, 'Incorrect number format, record is not updated!!')
            else:
                if Customer.objects.filter(mobile = mobile).exclude(id = user.id).exists():
                    messages.error(request, 'Mobile already exists')

                    if len(re.findall(r'\d', user.surname)) > 0 | len(re.findall(r'\d', user.name)) > 0:
                        messages.error(request, 'Invalid name or surname')
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
def filter_user_orders_by_date(request):
    user_id = request.user.id

    if request.method == "POST":

        deta1 =  request.POST['from']
        deta2 =  request.POST['to']
        print('my dates',deta1,deta2)
        try:
            date_obj_from = datetime.strptime(deta1, '%Y-%m-%d')
            date_obj_to = datetime.strptime(deta2, '%Y-%m-%d')
            # Do something with the valid date object

            if date_obj_to > date_obj_from:
                print('yes')
                orders = Order.objects.filter(user_id=user_id).filter(billing_status=True).filter(created__range=[date_obj_from,date_obj_to])
                return render(request, "account/dashboard/user_order_report.html", {"orders": orders})
            elif date_obj_to == date_obj_from:
                messages.error(request, 'Please use the minimum of one day')
                return render(request, "admin/admin_orders_report.html")
            else:
                print('incorrect dates')
                messages.error(request, 'Incorrect date, From date must be less than To date')
                return render(request, "account/dashboard/user_order_report.html")
        except ValueError:
            # Handle the case where the input is not a valid date
            print('Invalid date')
            messages.error(request, 'Invalid date')
            return render(request, "account/dashboard/user_order_report.html")
    
    return render(request, "account/dashboard/user_order_report.html")

@login_required
def filter_user_orders(request):
    user_id = request.user.id

    if request.method == "POST":

        deta =  request.POST['filter']

        print("sorting========>",deta)
        if deta == '2-Weeks':
            two_weeks_ago = datetime.now() - relativedelta(weeks=2)
            orders = Order.objects.filter(user_id=user_id, billing_status=True, created__range=(two_weeks_ago, datetime.now()))
            print(orders)

            return render(request, "account/dashboard/user_order_report.html", {"orders": orders})

        if deta == '1-months':
            one_month_ago = datetime.now() - relativedelta(months=1)
            orders = Order.objects.filter(user_id=user_id, billing_status=True, created__range=(one_month_ago, datetime.now()))
            print(orders)

            return render(request, "account/dashboard/user_order_report.html", {"orders": orders})
        if deta == '2-months':
            one_month_ago = datetime.now() - relativedelta(months=2)
            orders = Order.objects.filter(user_id=user_id, billing_status=True, created__range=(one_month_ago, datetime.now()))
            print(orders)

            return render(request, "account/dashboard/user_order_report.html", {"orders": orders})
        if deta == '3-months':
            one_month_ago = datetime.now() - relativedelta(months=3)
            orders = Order.objects.filter(user_id=user_id, billing_status=True, created__range=(one_month_ago, datetime.now()))
            print(orders)

            return render(request, "account/dashboard/user_order_report.html", {"orders": orders})

    # orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    return render(request, "account/dashboard/user_order_report.html")

@login_required
def admin_customers_report(request):
    print(request.method)
    if request.method == "POST":

        deta =  request.POST['filter']

        print('=================>',deta)

        if deta == '18-25':

            customers = Customer.objects.filter(is_staff=False).filter(Q(age_number__gte=18) & Q(age_number__lte=25))
            return render(request, "admin/admin_customers_report.html", {'customers':customers})
        if deta == '26-35':

            customers = Customer.objects.filter(is_staff=False).filter(Q(age_number__gte=26) & Q(age_number__lte=35))
            return render(request, "admin/admin_customers_report.html", {'customers':customers})
        if deta == '36-45':

            customers = Customer.objects.filter(is_staff=False).filter(Q(age_number__gte=36) & Q(age_number__lte=45))
            return render(request, "admin/admin_customers_report.html", {'customers':customers})
        if deta == '46+':

            customers = Customer.objects.filter(is_staff=False).filter(Q(age_number__gte=46))
            return render(request, "admin/admin_customers_report.html", {'customers':customers})
    
    return render(request, "admin/admin_customers_report.html")

@login_required
def filter_user_admin_by_date(request):

    if request.method == "POST":

        deta1 =  request.POST['from']
        deta2 =  request.POST['to']
        print('my dates',deta1,deta2)
        try:
            date_obj_from = datetime.strptime(deta1, '%Y-%m-%d')
            date_obj_to = datetime.strptime(deta2, '%Y-%m-%d')
            # Do something with the valid date object

            if date_obj_to > date_obj_from:
                print('yes')
                customers = Customer.objects.filter(is_staff=False).filter(created__range=[date_obj_from,date_obj_to])
                return render(request, "admin/admin_customers_report.html", {'customers':customers})
            elif date_obj_to == date_obj_from:
                messages.error(request, 'Please use the minimum of one day')
                return render(request, "admin/admin_customers_report.html")
            else:
                print('incorrect dates')
                messages.error(request, 'Incorrect date, From date must be less than To date')
                return render(request, "admin/admin_customers_report.html")
        except ValueError:
            # Handle the case where the input is not a valid date
            print('Invalid date')
            messages.error(request, 'Invalid date')
            return render(request, "admin/admin_customers_report.html")
    

@login_required
def user_orders(request):

    user_id = request.user.id

    if request.method == "POST":
        deta =  request.POST['sort']

        print("sorting========>",deta)
        if deta == 'Decending':
            orders = Order.objects.filter(user_id=user_id).filter(billing_status=True).order_by('-created')
            return render(request, "account/dashboard/user_orders.html", {"orders": orders})
        elif deta == "Ascending":
            orders = Order.objects.filter(user_id=user_id).filter(billing_status=True).order_by('created')
            return render(request, "account/dashboard/user_orders.html", {"orders": orders})
        else:
            orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
            return render(request, "account/dashboard/user_orders.html", {"orders": orders})

    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    return render(request, "account/dashboard/user_orders.html", {"orders": orders})

@login_required
def user_order_search(request):
    user_id = request.user.id
    print(request.method)
    orders = Order.objects.filter(user_id=user_id)
    if request.method == "POST":
        deta =  request.POST['search_data']

        print("---------->",deta)

        if(deta.isnumeric()):
            if deta == "":
                print("nothing")
                messages.error(request, 'Please insert something')
            else:
                orders = Order.objects.filter(user_id=user_id).filter(id=deta)
                return render(request, "account/dashboard/user_orders.html", {"orders": orders})
            # return render(request, "admin/orders.html", {"orders": orders})
        else:
            messages.error(request, 'Wrong input')
            
        return render(request, "account/dashboard/user_orders.html", {"orders": orders})
    
@login_required
def order_detail(request):
    user_id = request.user.id

    order_id = request.GET['order_id']

    order_id = order_id.replace("/", "" )
    print('---------->',order_id)

    option = OrderDeliveryOption.objects.filter(order=order_id[0])
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True).filter(id=order_id)
    for op in option:
        delivery_option = DeliveryOptions.objects.filter(id=op.delivery_option)
    
    
    return render(request, "account/dashboard/order_detail.html",{"orders": orders, 'delivery_option':delivery_option})

@login_required
def order_detail_admin(request):

    order_id = request.GET['order_id']
    order_id = order_id.replace("/","")

    print("============>",order_id)

    option = OrderDeliveryOption.objects.filter(order=order_id[0])
    orders = Order.objects.filter(billing_status=True).filter(id=order_id)
    for op in option:
        delivery_option = DeliveryOptions.objects.filter(id=op.delivery_option)
    
    
    return render(request, "account/dashboard/order_detail.html",{"orders": orders, 'delivery_option':delivery_option})

class CustomersListView(viewsets.ModelViewSet):
    serializer_class = CustomersSerializer
    queryset = Customer.objects.all()


class AddressListView(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()