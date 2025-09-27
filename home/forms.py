from django import forms
from .models import Appointment,ContactAdmin

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = '__all__'



class ContactAdminForm(forms.ModelForm):
    class Meta:
        model = ContactAdmin  
        fields = '__all__'  

# home/forms.py

from django import forms
from .models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        # List the fields you want to be editable
        fields = [
            'full_name', 'phone_number', 'street_address',
            'city', 'state', 'postal_code',
            'landmark', 'address_type'
        ]
        # Optional: Add Bootstrap classes to your form fields
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'street_address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'landmark': forms.TextInput(attrs={'class': 'form-control'}),
            'address_type': forms.Select(attrs={'class': 'form-select'}),
        }
        