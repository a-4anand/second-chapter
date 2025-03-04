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