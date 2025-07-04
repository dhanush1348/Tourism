from django import forms
from allauth.account.forms import SignupForm, LoginForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import User
from django.shortcuts import redirect
from django.urls import reverse

class CustomLoginForm(forms.Form):
    username = forms.CharField(label=_('Username'))
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise ValidationError(_("Username is required"))
        return username

class CustomSignupForm(forms.Form):
    username = forms.CharField(max_length=150, label=_('Username'))
    first_name = forms.CharField(max_length=30, label=_('First Name'))
    last_name = forms.CharField(max_length=30, label=_('Last Name'))
    email = forms.EmailField(label=_('Email'))
    date_of_birth = forms.DateField(
        label=_('Date of Birth'),
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    phone_number = forms.CharField(max_length=15, label=_('Phone Number'))
    address = forms.CharField(
        max_length=255,
        label=_('Address'),
        widget=forms.Textarea(attrs={'rows': 3})
    )
    city = forms.CharField(max_length=100, label=_('City'))
    country = forms.CharField(max_length=100, label=_('Country'))
    postal_code = forms.CharField(max_length=20, label=_('Postal Code'))
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput,
        min_length=8
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise ValidationError(_("Username is required"))
        if User.objects.filter(username=username).exists():
            raise ValidationError(_("This username is already taken"))
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError(_("Email is required"))
        if User.objects.filter(email=email).exists():
            raise ValidationError(_("This email is already in use"))
        return email

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if not phone:
            raise ValidationError(_("Phone number is required"))
        return phone

    def save(self):
        # Create a new user with the form data
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            date_of_birth=self.cleaned_data['date_of_birth'],
            phone_number=self.cleaned_data['phone_number'],
            address=self.cleaned_data['address'],
            city=self.cleaned_data['city'],
            country=self.cleaned_data['country'],
            postal_code=self.cleaned_data['postal_code']
        )
        return user 