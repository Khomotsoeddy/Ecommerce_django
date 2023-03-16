from django import forms
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm,
                                       SetPasswordForm)

from .models import Customer, Address
import re

class UserAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["full_name", "phone", "address_line", "address_line2", "town_city", "postcode"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["full_name"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Recipient Full Name"}
        )
        self.fields["phone"].widget.attrs.update({"class": "form-control mb-2 account-form", "placeholder": "Phone"})
        self.fields["address_line"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Street Name"}
        )
        self.fields["address_line2"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Surbub Name"}
        )
        self.fields["town_city"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "City"}
        )
        self.fields["postcode"].widget.attrs.update(
            {"class": "form-control mb-2 account-form", "placeholder": "Postal code"}
        )



class UserLoginForm(AuthenticationForm):

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Username', 'id': 'login-username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'id': 'login-pwd',
        }
    ))


class RegistrationForm(forms.ModelForm):

    # user_name = forms.CharField(
    #     label='Enter Username', min_length=4, max_length=50, help_text='Required')
    name = forms.CharField(
        label='Enter name', min_length=4, max_length=50, help_text='Required')
    mobile = forms.CharField(
        label='Phone number', min_length=4, max_length=50, help_text='Required')
    id_number = forms.CharField(
        label='Identity number', min_length=13, max_length=13, help_text='Required', error_messages={
        'required': 'Sorry, you will need an ID Number'})
    email = forms.EmailField(max_length=100, help_text='Required', error_messages={
        'required': 'Sorry, you will need an email'})
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = Customer
        fields = ('name','mobile', 'email','id_number')
    
    def clean_id_number(self):
        id_number = self.cleaned_data['id_number']
        if Customer.objects.filter(id_number=id_number).exists():
            raise forms.ValidationError("Id number already exists")
        return id_number
    
    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        if(len(mobile) != 12):
            raise forms.ValidationError("Incorrect format")
        else:
            pattern=r"[+27][^.......$]"  
            match = re.match(pattern,mobile) 
            if not match:
                raise forms.ValidationError("Incorrect format")
        return mobile

    def clean_password2(self):
        cd = self.cleaned_data
        
        if len(cd['password']) < 7:
            raise forms.ValidationError('Passwords is short.')
        else:
            if cd['password'] != cd['password2']:
                raise forms.ValidationError('Passwords do not match.')
            return cd['password2']
 
    def clean_email(self):
        email = self.cleaned_data['email']
        if Customer.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Please use another Email, that is already taken')
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Name'})
        self.fields['mobile'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Mobile (+27711110000)'})
        self.fields['id_number'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'ID Number'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'E-mail', 'name': 'email', 'id': 'id_email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Repeat Password'})


class PwdResetForm(PasswordResetForm):

    email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'form-email'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        u = Customer.objects.filter(email=email)
        if not u:
            raise forms.ValidationError(
                'Unfortunatley we can not find that email address')
        return email


class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-newpass'}))
    new_password2 = forms.CharField(
        label='Repeat password', widget=forms.PasswordInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-new-pass2'}))


class UserEditForm(forms.ModelForm):

    email = forms.EmailField(
        label='Account email (can not be changed)', max_length=200, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'form-email', 'readonly': 'readonly'}))
    id_number = forms.EmailField(
        label='Identity Number(can not be changed)', max_length=200, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'ID Number', 'id': 'form-idnumber', 'readonly': 'readonly'}))
    gender = forms.EmailField(
        label='Gender(can not be changed)', max_length=200, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Gender', 'id': 'form-gender', 'readonly': 'readonly'}))
    date_of_birth = forms.EmailField(
        label='Identity Number(can not be changed)', max_length=200, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Date of Birth', 'id': 'form-date_of_birth', 'readonly': 'readonly'}))

    user_name = forms.CharField(
        label='Firstname', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Username', 'id': 'form-firstname', 'readonly': 'readonly'}))

    name = forms.CharField(
        label='Firstname', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Firstname', 'id': 'form-lastname'}))
    mobile = forms.CharField(
        label='Mobile', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Mobile (+27711110000)', 'id': 'form-lastname'}))
    
    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']

        if(len(mobile) != 12):
            raise forms.ValidationError("Incorrect format")
        else:
            pattern=r"[+27][^.......$]"  
            match = re.match(pattern,mobile) 
            if not match:
                raise forms.ValidationError("Incorrect format")
        return mobile

    class Meta:
        model = Customer
        fields = ('email','name','mobile','id_number', 'date_of_birth', 'gender')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].required = True
        self.fields['email'].required = True
        self.fields['id_number'].required = True
        self.fields['date_of_birth'].required = True
        self.fields['gender'].required = True
