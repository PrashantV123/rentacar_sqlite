from django import forms
from .models import Reservation, Vehicle
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = '__all__'
        labels = {'customer': 'Dealer', 'licensenm': 'License #'}

        widgets = {
            'customer': forms.Select(attrs={'class': 'form-control', 'type': 'select'}),
            'model': forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}),
            'type': forms.Select(attrs={'class': 'form-control', 'type': 'select'}),
            'rate': forms.NumberInput(attrs={'class': 'form-control', 'type': 'number'}),
            'licensenm': forms.TextInput(attrs={'class': 'form-control'}),
            'available_at': forms.Select(attrs={'class': 'form-control', 'type': 'select'}),
        }


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ('pickup_date', 'return_date', 'pickup_location',
                  'return_location', 'type')

        widgets = {
            'pickup_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'return_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'pickup_location': forms.Select(attrs={'class': 'form-control', 'type': 'select'}),
            'return_location': forms.Select(attrs={'class': 'form-control', 'type': 'select'}),
            'type': forms.Select(attrs={'class': 'form-control', 'type': 'select'}),
        }


class AddReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        # fields = '__all__'
        exclude = ['reservation_status']
        labels = {'licensenm': 'License #'}
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-control'}),
            'vehicle': forms.Select(attrs={'class': 'form-control'}),
            'pickup_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'return_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'pickup_location': forms.Select(attrs={'class': 'form-control', 'type': 'select'}),
            'return_location': forms.Select(attrs={'class': 'form-control', 'type': 'select'}),
            'type': forms.Select(attrs={'class': 'form-control', 'type': 'select'}),
            'days_rented': forms.NumberInput(attrs={'class': 'form-control'}),
            'order_total': forms.NumberInput(attrs={'class': 'form-control'}),

        }


class customer_signup_form(UserCreationForm):
    password1 = forms.CharField(
        label='Password:', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password (again):',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter valid email address'})
        }


class dealer_signup_form(UserCreationForm):
    password1 = forms.CharField(
        label='Password:', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password (again):',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter TOWN-STATE-RACC i.e PARSIPPANY-NJ-RACC"}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': "Enter Dealership Manager's e-mail address"})
        }


class user_login_form(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(
        attrs={'autofocus': True, 'class': 'form-control'}))
    password = forms.CharField(label=_('Password'), strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'current-password', 'class': 'form-control'}))
